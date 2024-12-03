import pandas as pd
import sqlite3
import json

def extract_data(file_path):
    try:
        data = pd.read_excel(file_path)
        return data
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def transform_data(df_a, df_b):
    df_a["region"] = "A"
    df_b["region"] = "B"
    combined_data = pd.concat([df_a, df_b], ignore_index=True)
    combined_data["PromotionDiscount"] = combined_data["PromotionDiscount"].apply(
        lambda x: float(json.loads(x)["Amount"]) if isinstance(x, str) else 0
    )
    combined_data["QuantityOrdered"] = combined_data["QuantityOrdered"].astype(float).astype(int)
    combined_data["total_sales"] = combined_data["QuantityOrdered"] * combined_data["ItemPrice"]
    combined_data["net_sale"] = combined_data["total_sales"] - combined_data["PromotionDiscount"]
    combined_data = combined_data.drop_duplicates(subset=["OrderId", "region"])
    transformed_data = combined_data[combined_data["net_sale"] > 0]
    return transformed_data

def load_data_to_db(data, db_name="sales_data.db"):
    conn = sqlite3.connect(db_name)
    data.to_sql("sales_data", conn, if_exists="replace", index=False)
    conn.close()
    print("Data successfully loaded into the database.")

def validate_data(db_name="sales_data.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    queries = {
        "total_records": "SELECT COUNT(*) FROM sales_data;",
        "total_sales_by_region": "SELECT region, SUM(total_sales) FROM sales_data GROUP BY region;",
        "average_sales_per_transaction": "SELECT AVG(net_sale) FROM sales_data;",
        "check_duplicates": "SELECT OrderId, COUNT(*) FROM sales_data GROUP BY OrderId HAVING COUNT(*) > 1;",
    }

    for description, query in queries.items():
        cursor.execute(query)
        result = cursor.fetchall()

        if description == "check_duplicates":
            if result:
                print(f"Found {len(result)} duplicate OrderIds.")
            else:
                print("No duplicates found.")
        else:
            print(f"{description}: {result}")

    conn.close()


def main():
    file_a = "order_region_a.xlsx"
    file_b = "order_region_b.xlsx"
    df_a = extract_data(file_a)
    df_b = extract_data(file_b)
    if df_a is not None and df_b is not None:
        transformed_data = transform_data(df_a, df_b)
        load_data_to_db(transformed_data)
        validate_data()
    else:
        print("Failed to extract data.")

if __name__ == "__main__":
    main()
    
