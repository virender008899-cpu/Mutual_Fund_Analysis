import pandas as pd
import requests
import os

# Create output folder
output_path = "data/raw"
os.makedirs(output_path, exist_ok=True)

# Scheme codes
schemes = {
    "HDFC_Top_100": "125497",
    "SBI_Bluechip": "119551",
    "ICICI_Bluechip": "120503",
    "Nippon_Large_Cap": "118632",
    "Axis_Bluechip": "119092",
    "Kotak_Bluechip": "120841"
}

# Fetch NAV data
for name, code in schemes.items():

    url = f"https://api.mfapi.in/mf/{code}"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()

        df = pd.DataFrame(data["data"])

        df["scheme_code"] = code
        df["scheme_name"] = data["meta"]["scheme_name"]

        # Save CSV
        file_path = os.path.join(
            output_path, f"{name}_NAV.csv"
        )

        df.to_csv(file_path, index=False)

        print(name, "Saved:", df.shape)

    except requests.exceptions.RequestException as error:
        print(name, "API Error:", error)

    except (KeyError, ValueError, TypeError) as error:
        print(name, "Data Error:", error)


print("\nNAV data fetching process completed.")


# Display saved NAV data

for name, code in schemes.items():

    file_path = os.path.join(
        output_path, f"{name}_NAV.csv"
    )

    if os.path.exists(file_path):

        df = pd.read_csv(file_path)

        print("\nDataset:", name)

        # Display Date, NAV and Scheme Code
        print(df[["date", "nav", "scheme_code"]].head(10))

        print("Shape:", df.shape)

    else:
        print(name, "CSV file not available.")