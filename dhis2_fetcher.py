import requests
import json
import csv
from datetime import datetime
from requests.auth import HTTPBasicAuth

# Configuration
API_URL = "http://cmis.moh.go.tz/api/tracker/enrollments?program=CYm744mxGv2&orgUnit=RqA7Tf2z2wz&ouMode=DESCENDANTS&paging=false"

# Your DHIS2 credentials
USERNAME = "hmkama"  # Replace with your actual username
PASSWORD = "Cmis@2025"  # Replace with your actual password

# Tracked Entity Attributes to extract
TRACKED_ATTRIBUTES = {
    'xeuwJUX1kZT': 'SMPS 4 : Namba Ya Utambulisho Wa Kijiji',
    'ctBYc8eEQ84': 'SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa'
}

# Data Elements to extract with their labels
DATA_ELEMENTS = {
    'SXdSBe7lbZU': 'SMPS 4. 91. Namba ya mstari ya mwanakaya',
    'D8t7JCm6YMc': 'SMPS 4: Jinsia',
    'c7BbgnMofyL': 'SMPS 4. 92. Jina la Kwanza',
    'ywDhTy7oIao': 'SMPS 4. 92. Jina la Kati',
    'SbGy0VUSLiK': 'SMPS 4. 92. Jina la Ukoo',
    'Bqg77A7t8dO': 'SMPS 4. 93. Uhusiano wa mwanakaya na mkuu wa kaya',
    'DeYoF4D1L4k': 'SMPS 4. Je, mwanakaya ana umri gani?',
    'lsOHSMltipn': 'SMPS 4. Ingiza umri wa mwanakaya kwa miezi',
    'tHJTXtRMfGx': 'SMPS 4 Control',
    'm1yns3orW89': 'SMPS 4 Pf',
    'kMPnzu9MzdR': 'SMPS 4 Pan',
    'IWeuZu87y9x': 'SMPS 4 Tafsiri ya Kipimo cha malaria',
    'ldUn1IEk1qS': 'SMPS 4. Kama matokeo ya kipimo ni chanya. Je, amepatiwa dawa?',
    't8ieA7heRcX': 'SMPS 4: Aina ya Alu aliyopewa',
    'bVuGJLDBPjb': 'SMPS 4: Idadi ya vidonge alivyopewa kulingana na uzito na umri (Link na uzito uliochukuliwa kwenye general information) Min vidonge 6 and Max 24',
    'ESGTOW9P932': 'SMPS 4 Je, amepimwa kiwango cha wingi wa damu?',
    'v2JhdNaMGw9': 'SMPS 4. Kama hapana toa sababu',
    'AUev4BOeZ0d': 'SMPS 4 Kiwango/wingi wa damu (Hb-g/dl)',
    'fULaxdVs1K6': 'SMPS 4: MUAC (5cm-20cm)'
}


def fetch_data(url, username, password):
    """Fetch data from DHIS2 API with authentication."""
    print("Fetching data from API...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(
            url,
            auth=HTTPBasicAuth(username, password),
            headers={'Content-Type': 'application/json'},
            timeout=60
        )
        
        response.raise_for_status()
        print(f"✓ Data fetched successfully (Status: {response.status_code})")
        print(f"Response length: {len(response.text)} characters")
        
        # Save raw response
        with open('raw_response.json', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("✓ Raw response saved to: raw_response.json")
        
        if not response.text or response.text.strip() == '':
            print("⚠ WARNING: Response is empty!")
            return {}
        
        return response.json()
    
    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP Error: {e}")
        print(f"  Response: {e.response.text if e.response else 'No response'}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"✗ Request Error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"✗ JSON Decode Error: {e}")
        print(f"  Response text (first 500 chars): {response.text[:500]}")
        return None


def get_org_unit_name(org_unit_id, username, password):
    """Fetch organization unit name from DHIS2 API."""
    try:
        url = f"http://cmis.moh.go.tz/api/organisationUnits/{org_unit_id}.json?fields=name"
        response = requests.get(
            url,
            auth=HTTPBasicAuth(username, password),
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return data.get('name', org_unit_id)
    except:
        pass
    return org_unit_id


def flatten_enrollments(enrollments, username, password):
    """Flatten enrollments into rows with one row per event/household member."""
    print(f"\nFlattening {len(enrollments)} enrollments into rows...")
    
    rows = []
    org_unit_cache = {}
    
    for enrollment in enrollments:
        # Get basic enrollment info
        org_unit_id = enrollment.get('orgUnit', '')
        
        # Get org unit name (with caching)
        if org_unit_id not in org_unit_cache:
            org_unit_cache[org_unit_id] = get_org_unit_name(org_unit_id, username, password)
        org_unit_name = org_unit_cache[org_unit_id]
        
        # Extract tracked entity attributes
        attributes = {}
        if 'attributes' in enrollment:
            for attr in enrollment['attributes']:
                attr_id = attr.get('attribute')
                if attr_id in TRACKED_ATTRIBUTES:
                    attributes[attr_id] = attr.get('value', '')
        
        # Process events (each event = one household member)
        if 'events' in enrollment and enrollment['events']:
            for event in enrollment['events']:
                row = {
                    'Organisation unit name': org_unit_name
                }
                
                # Add tracked attributes
                for attr_id, label in TRACKED_ATTRIBUTES.items():
                    row[label] = attributes.get(attr_id, '')
                
                # Extract data values from this event
                event_data = {}
                if 'dataValues' in event:
                    for dv in event['dataValues']:
                        element_id = dv.get('dataElement')
                        if element_id in DATA_ELEMENTS:
                            event_data[element_id] = dv.get('value', '')
                
                # Add data elements
                for elem_id, label in DATA_ELEMENTS.items():
                    row[label] = event_data.get(elem_id, '')
                
                rows.append(row)
        else:
            # If no events, create one row with just the enrollment data
            row = {
                'Organisation unit name': org_unit_name
            }
            
            for attr_id, label in TRACKED_ATTRIBUTES.items():
                row[label] = attributes.get(attr_id, '')
            
            for elem_id, label in DATA_ELEMENTS.items():
                row[label] = ''
            
            rows.append(row)
    
    print(f"✓ Created {len(rows)} rows")
    return rows


def save_to_csv(rows, filename=None):
    """Save flattened data to CSV file."""
    if filename is None:
        filename = f"dhis2_smps4_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    if not rows:
        print("✗ No data to save")
        return
    
    # Get headers in the correct order
    headers = ['Organisation unit name']
    headers.extend(TRACKED_ATTRIBUTES.values())
    headers.extend(DATA_ELEMENTS.values())
    
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"✓ CSV saved to: {filename}")


def save_to_excel(rows, filename=None):
    """Save flattened data to Excel file (requires openpyxl)."""
    try:
        import openpyxl
        from openpyxl import Workbook
        
        if filename is None:
            filename = f"dhis2_smps4_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        if not rows:
            print("✗ No data to save")
            return
        
        wb = Workbook()
        ws = wb.active
        ws.title = "SMPS 4 Data"
        
        # Get headers
        headers = ['Organisation unit name']
        headers.extend(TRACKED_ATTRIBUTES.values())
        headers.extend(DATA_ELEMENTS.values())
        
        # Write headers
        ws.append(headers)
        
        # Write data rows
        for row in rows:
            ws.append([row.get(h, '') for h in headers])
        
        wb.save(filename)
        print(f"✓ Excel saved to: {filename}")
        
    except ImportError:
        print("⚠ openpyxl not installed. Skipping Excel export.")
        print("  Install with: pip install openpyxl")


def main():
    """Main function to fetch and process DHIS2 data."""
    print("=" * 60)
    print("DHIS2 SMPS 4 Data Extractor")
    print("=" * 60)
    
    # Fetch data from API
    result = fetch_data(API_URL, USERNAME, PASSWORD)
    
    if result is None:
        print("\n✗ Failed to fetch data. Please check your credentials and API URL.")
        return
    
    # Debug info
    print("\n--- API Response Structure ---")
    print(f"Response type: {type(result)}")
    
    if isinstance(result, dict):
        print(f"Top-level keys: {list(result.keys())}")
    
    # Try to find enrollments in the response
    enrollments = None
    possible_keys = ['instances', 'enrollments', 'trackedEntityInstances', 'data']
    
    for key in possible_keys:
        if key in result and result[key]:
            enrollments = result[key]
            print(f"✓ Found {len(enrollments)} enrollments under key: '{key}'")
            break
    
    if enrollments is None or not enrollments:
        print("\n⚠ No enrollments found in the response!")
        print("\nPossible reasons:")
        print("  1. No data exists for this program/orgUnit combination")
        print("  2. Check if program ID (CYm744mxGv2) is correct")
        print("  3. Check if orgUnit ID (RqA7Tf2z2wz) is correct")
        print("  4. You might need different filters or date ranges")
        print("\nCheck 'raw_response.json' to inspect the actual response")
        return
    
    # Flatten enrollments to rows
    rows = flatten_enrollments(enrollments, USERNAME, PASSWORD)
    
    if not rows:
        print("\n✗ No rows generated from enrollments")
        return
    
    # Save to files
    print("\nSaving data...")
    save_to_csv(rows)
    save_to_excel(rows)
    
    print("\n" + "=" * 60)
    print("✓ Processing complete!")
    print(f"  Total rows: {len(rows)}")
    print(f"  Tracked attributes: {len(TRACKED_ATTRIBUTES)}")
    print(f"  Data elements: {len(DATA_ELEMENTS)}")
    print("=" * 60)


if __name__ == "__main__":
    main()