import sqlite3

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS laptops (
        name TEXT,
        rating TEXT,
        price INT,
        url TEXT UNIQUE,
        articlenumber INT UNIQUE,
        manufacturercode TEXT,
        brand TEXT,
        warranty TEXT,
        handling_of_your_defect TEXT,
        old_device_return_for_free TEXT,
        screen_diagonal INT,
        internal_ram_memory INT,
        graphics_card_chipset TEXT,
        touchscreen TEXT,
        usb_type TEXT,
        Recommended_usage TEXT,
        speed_class TEXT,
        build_quality TEXT,
        screen_resolution TEXT,
        screen_resolution_width INT,
        screen_resolution_height INT,
        refresh_rate INT,
        screen_reflection TEXT,
        paneltype TEXT,
        adaptive_sync TEXT,
        processor_name TEXT,
        processor_number TEXT,
        processor_core TEXT,
        processor_codename TEXT,
        processor_clockspeed INT,
        processor_clockspeed_turbo INT,
        processor_cachememory INT,
        processor_intelevolaptop TEXT,
        intern_ram INT,
        ram_composition TEXT,
        ram_slot_1 TEXT,
        ram_slots TEXT,
        storage_type TEXT,
        total_storage_capacity INT,
        ssd_storage_capacity INT,
        storage_disk_type TEXT,
        gpu_chipset TEXT,
        gpu_type TEXT,
        operating_system TEXT,
        operating_system_language TEXT,
        model_laptop TEXT,
        color TEXT,
        material TEXT,
        height TEXT,
        width TEXT,
        depth TEXT,
        weight TEXT,
        mobile_dataconnection TEXT,
        bluetooth TEXT,
        bluetooth_version TEXT,
        usb_connection TEXT,
        amount_of_usb_connections TEXT,
        usb_connection_type TEXT,
        protocol_female_usb_c_port TEXT,
        usb_version_female_usb_c_port TEXT,
        video_output_via_usb_c_port TEXT,
        hdmi_connection TEXT,
        displayport_connection TEXT,
        vga_connection TEXT,
        thunderbolt_connection TEXT,
        headphone_jack TEXT,
        keyboard_layout TEXT,
        physical_keyboard_layout TEXT,
        numeric_keyboard TEXT,
        stain_resistant TEXT,
        keyboard_backlight TEXT,
        mechanical_keyboard TEXT,
        programmable_keys TEXT,
        microphone TEXT,
        amount_of_speakers INT,
        audio_type TEXT,
        audio_brand TEXT,
        built_in_camera TEXT,
        camera_resolution INT,
        battery_type TEXT,
        battery_capacity INT,
        factory_guarantee TEXT,
        TPM TEXT,
        kensington_lock TEXT,
        windows_hello TEXT,
        fingerprint_sensor TEXT,
        security_class TEXT,
        amount_of_free_ram_slots INT,
        extra_software TEXT
    )
    """)
    conn.commit()

import sqlite3
import re

import re

def extract_numeric(value, is_storage=False, is_price=False):
    """
    Extracts numeric values from strings.
    - Converts TB to GB if is_storage=True.
    - Cleans up price formatting and converts to integer if is_price=True.
    """
    if not value or not isinstance(value, str):
        return None  # Return None for empty or invalid input

    value = value.strip()  # Remove leading/trailing spaces

    # Handle price conversion (e.g., "€1.209,-" → "1209")
    if is_price:
        value = re.sub(r'[^\d,]', '', value)  # Remove all non-numeric & keep comma
        value = value.replace(',', '')  # Remove comma in "1.209" (European format)
        
        return int(value) if value.isdigit() else None

    # Convert TB to GB if needed
    if is_storage and "TB" in value:
        num = re.search(r'\d+(\.\d+)?', value)  # Extract number
        return int(float(num.group()) * 1024) if num else None

    # Extract numeric part for other values
    num_match = re.search(r'\d+', value)
    return int(num_match.group()) if num_match else None



def insert_laptop_data(conn, item):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR IGNORE INTO laptops (
        name, rating, price, url, articlenumber, manufacturercode, brand, warranty,
        handling_of_your_defect, old_device_return_for_free,
        screen_diagonal, internal_ram_memory, graphics_card_chipset, touchscreen, usb_type, Recommended_usage,
        speed_class, build_quality, screen_resolution, screen_resolution_width,
        screen_resolution_height, refresh_rate, screen_reflection, paneltype, adaptive_sync,
        processor_name, processor_number, processor_core, processor_codename, processor_clockspeed,
        processor_clockspeed_turbo, processor_cachememory, processor_intelevolaptop, intern_ram,
        ram_composition, ram_slot_1, ram_slots, storage_type,
        total_storage_capacity, ssd_storage_capacity, storage_disk_type, gpu_chipset, gpu_type, operating_system,
        operating_system_language, model_laptop, color, material, height, width, depth, weight,
        mobile_dataconnection, bluetooth, bluetooth_version, usb_connection,
        amount_of_usb_connections, usb_connection_type, protocol_female_usb_c_port,
        usb_version_female_usb_c_port, video_output_via_usb_c_port, hdmi_connection,
        displayport_connection, vga_connection, thunderbolt_connection, headphone_jack,
        keyboard_layout, physical_keyboard_layout, numeric_keyboard, stain_resistant,
        keyboard_backlight, mechanical_keyboard, programmable_keys, microphone, amount_of_speakers,
        audio_type, audio_brand, built_in_camera, camera_resolution, battery_type, battery_capacity,
        factory_guarantee, TPM, kensington_lock, windows_hello, fingerprint_sensor, security_class, 
        amount_of_free_ram_slots, extra_software
    ) VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    )
    """, (
        item.get("name", ""),
        item.get("rating", ""),
        extract_numeric(item.get("price", ""), is_price=True),
        item["url"],
        extract_numeric(item.get("articlenumber", "")),
        item.get("manufacturercode", ""),
        item.get("brand", ""),
        item.get("warranty", ""),
        item.get("handling_of_your_defect", ""),
        item.get("old_device_return_for_free", ""),
        extract_numeric(item.get("screen_diagonal", "")),  # Convert to int
        extract_numeric(item.get("internal_ram_memory", "")),  # Convert to int
        item.get("graphics_card_chipset", ""),
        item.get("touchscreen", ""),
        item.get("usb_type", ""),
        item.get("Recommended_usage", ""),
        item.get("speed_class", ""),
        item.get("build_quality", ""),
        item.get("screen_resolution", ""),
        extract_numeric(item.get("screen_resolution_width", "")),  # Convert to int
        extract_numeric(item.get("screen_resolution_height", "")),  # Convert to int
        extract_numeric(item.get("refresh_rate", "")),  # Convert to int
        item.get("screen_reflection", ""),
        item.get("paneltype", ""),
        item.get("adaptive_sync", ""),
        item.get("processor_name", ""),
        item.get("processor_number", ""),
        item.get("processor_core", ""),
        item.get("processor_codename", ""),
        extract_numeric(item.get("processor_clockspeed", "")),  # Convert to int
        extract_numeric(item.get("processor_clockspeed_turbo", "")),  # Convert to int
        extract_numeric(item.get("processor_cachememory", "")),  # Convert to int
        item.get("processor_intelevolaptop", ""),
        extract_numeric(item.get("intern_ram", "")),  # Convert to int
        item.get("ram_composition", ""),
        item.get("ram_slot_1", ""),
        item.get("ram_slots", ""),
        item.get("storage_type", ""),
        extract_numeric(item.get("total_storage_capacity", ""), is_storage=True),  # Convert to int
        extract_numeric(item.get("ssd_storage_capacity", ""), is_storage=True),  # Convert to int
        item.get("storage_disk_type", ""),
        item.get("gpu_chipset", ""),
        item.get("gpu_type", ""),
        item.get("operating_system", ""),
        item.get("operating_system_language", ""),
        item.get("model_laptop", ""),
        item.get("color", ""),
        item.get("material", ""),
        item.get("height", ""),
        item.get("width", ""),
        item.get("depth", ""),
        item.get("weight", ""),
        item.get("mobile_dataconnection", ""),
        item.get("bluetooth", ""),
        item.get("bluetooth_version", ""),
        item.get("usb_connection", ""),
        item.get("amount_of_usb_connections", ""),
        item.get("usb_connection_type", ""),
        item.get("protocol_female_usb_c_port", ""),
        item.get("usb_version_female_usb_c_port", ""),
        item.get("video_output_via_usb_c_port", ""),
        item.get("hdmi_connection", ""),
        item.get("displayport_connection", ""),
        item.get("vga_connection", ""),
        item.get("thunderbolt_connection", ""),
        item.get("headphone_jack", ""),
        item.get("keyboard_layout", ""),
        item.get("physical_keyboard_layout", ""),
        item.get("numeric_keyboard", ""),
        item.get("stain_resistant", ""),
        item.get("keyboard_backlight", ""),
        item.get("mechanical_keyboard", ""),
        item.get("programmable_keys", ""),
        item.get("microphone", ""),
        extract_numeric(item.get("amount_of_speakers", "")),
        item.get("audio_type", ""),
        item.get("audio_brand", ""),
        item.get("built_in_camera", ""),
        extract_numeric(item.get("camera_resolution", "")),
        item.get("battery_type", ""),
        extract_numeric(item.get("battery_capacity", "")),
        item.get("factory_guarantee", ""),
        item.get("TPM", ""),
        item.get("kensington_lock", ""),
        item.get("windows_hello", ""),
        item.get("fingerprint_sensor", ""),
        item.get("security_class", ""),
        extract_numeric(item.get("amount_of_free_ram_slots", "")),
        item.get("extra_software", "")
    ))
    conn.commit()
