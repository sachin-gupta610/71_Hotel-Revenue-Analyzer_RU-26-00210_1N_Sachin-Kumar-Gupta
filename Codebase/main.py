import os
import pandas as pd
import matplotlib.pyplot as plt


def load_and_clean_data(fname):
    df = pd.read_csv(fname)
    rows = []

    for i, r in df.iterrows():
        r_num = i + 2
        try:
            sold = float(r['RoomsSold'])
            rate = float(r['Rate'])
            if sold < 0 or rate < 0:
                print(f"Warning: Row {r_num} skipped - RoomsSold must be 0 or more.")
                continue
            rows.append({
                'Date': str(r['Date']).strip(),
                'RoomType': str(r['RoomType']).strip(),
                'RoomsSold': sold,
                'Rate': rate,
                'Revenue': sold * rate
            })
        except:
            print(f"Warning: Row {r_num} skipped - Invalid non-numeric values.")
            continue

    return pd.DataFrame(rows)


def show_daily_revenue(data):
    daily = data.groupby('Date')['Revenue'].sum()
    for d, rev in daily.items():
        print(f"{d} : Rs. {int(rev)}")
    print(f"Total revenue: Rs. {int(daily.sum())}")

    best_day = daily.idxmax()
    best_rev = int(daily.max())
    print(f"Best day: {best_day} (Rs. {best_rev})")

    daily.plot(kind='bar', color='skyblue')
    plt.title('Daily Revenue')
    plt.xlabel('Date')
    plt.ylabel('Revenue (Rs.)')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()


def show_room_type_revenue(data):
    rtype = data.groupby('RoomType', sort=False)['Revenue'].sum()
    tot = rtype.sum()
    for rt, rev in rtype.items():
        p = (rev / tot) * 100
        print(f"{rt} : Rs. {int(rev)} ({p:.2f}%)")
    print(f"Total revenue: Rs. {int(tot)}")

    rtype.plot(kind='pie', autopct='%1.2f%%')
    plt.title('Revenue by Room Type')
    plt.ylabel('')
    plt.tight_layout()
    plt.show()


def main():
    fname = input("Enter CSV filename (default: hotel_sales.csv): ").strip()
    if not fname:
        fname = "hotel_sales.csv"

    if not os.path.exists(fname):
        print(f"Error: File '{fname}' not found.")
        return

    data = load_and_clean_data(fname)
    if data.empty:
        print("No valid records found to analyse.")
        return

    print(f"Valid records analysed: {len(data)}")
    print("\nMenu:")
    print("1. Daily revenue")
    print("2. Revenue by room type")
    ch = input("Enter choice (1/2): ").strip()

    if ch == "1":
        show_daily_revenue(data)
    elif ch == "2":
        show_room_type_revenue(data)
    else:
        print("Invalid choice. Please enter 1 or 2.")


main()
