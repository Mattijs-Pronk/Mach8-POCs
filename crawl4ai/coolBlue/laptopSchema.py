laptopSchemaDTO = {
    "name": "Laptops",
    "baseSelector": ".product-page",
    "fields": [
        {
            "name": "name",
            "selector": ".js-product-name",
            "type": "text"
        },
        {
            "name": "rating",
            "selector": ".review-rating__reviews",
            "type": "text"
        },
        {
            "name": "price",
            "selector": ".sales-price__current",
            "type": "text"
        },
        # artikedingen
        {
            "name": "articlenumber",
            "selector": "[data-property-name='Artikelnummer'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "manufacturercode",
            "selector": "[data-property-name='Fabrikantcode'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "brand",
            "selector": "[data-property-name='Merk'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "warranty",
            "selector": "[data-property-name='Garantie'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "handling_of_your_defect",
            "selector": "[data-property-name='Afhandeling van je defect'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "old_device_return_for_free",
            "selector": "[data-property-name='Oude apparaat gratis retour'] .product-specs__item-spec",
            "type": "text"
        },
        # Belangrijke eigenschappen
        {
            "name": "internal_ram_memory",
            "selector": "[data-property-name='Intern werkgeheugen (RAM)'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "graphics_card_chipset",
            "selector": "[data-property-name='Videokaart chipset'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "touchscreen",
            "selector": "[data-property-name='Touchscreen'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "usb_type",
            "selector": "[data-property-name='Type usb-aansluiting'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "Recommended_usage",
            "selector": "[data-property-name='Aanbevolen voor gebruik laptops'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "speed_class",
            "selector": "[data-property-name='Snelheidsklasse laptops'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "build_quality",
            "selector": "[data-property-name='Bouwkwaliteit laptops'] .product-specs__item-spec",
            "type": "text"
        },
        # Scherm eigenschappen
        {
            "name": "screen_diagonal",
            "selector": "[data-property-name='Schermdiagonaal'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "screen_resolution",
            "selector": "[data-property-name='Scherpte'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "screen_resolution_width",
            "selector": "[data-property-name='Resolutie breedte'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "screen_resolution_height",
            "selector": "[data-property-name='Resolutie hoogte'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "refresh_rate",
            "selector": "[data-property-name='Verversingssnelheid'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "touch_screen",
            "selector": "[data-property-name='Touchscreen'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "screen_reflection",
            "selector": "[data-property-name='Reflectie scherm'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "paneltype",
            "selector": "[data-property-name='Paneeltype'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "adaptive_sync",
            "selector": "[data-property-name='Adaptive Sync'] .product-specs__item-spec",
            "type": "text"
        },
        # Processor eigenschappen
        {
            "name": "processor_name",
            "selector": "[data-property-name='Processor'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "processor_number",
            "selector": "[data-property-name='Processor cijfer'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "processor_core",
            "selector": "[data-property-name='Processor kernen'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "processor_codename",
            "selector": "[data-property-name='Processor codenaam'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "processor_clockspeed",
            "selector": "[data-property-name='Kloksnelheid'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "processor_clockspeed_turbo",
            "selector": "[data-property-name='Turbo snelheid'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "processor_cachememory",
            "selector": "[data-property-name='Cachegeheugen'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "processor_intelevolaptop",
            "selector": "[data-property-name='Intel evo laptop'] .product-specs__item-spec",
            "type": "text"
        },
        # Werkgeheugen eigenschappen
        {
            "name": "intern_ram",
            "selector": "[data-property-name='Intern werkgeheugen (RAM)'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "ram_composition",
            "selector": "[data-property-name='Samenstelling geheugen'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "ram_slot_1",
            "selector": "[data-property-name='Geheugenslot 1'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "ram_slots",
            "selector": "[data-property-name='Totaal aantal RAM geheugensloten'] .product-specs__item-spec",
            "type": "text"
        },
        # Opslag eigenschappen
        {
            "name": "storage_type",
            "selector": "[data-property-name='Type opslag'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "total_storage_capacity",
            "selector": "[data-property-name='Totale opslagcapaciteit'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "ssd_storage_capacity",
            "selector": "[data-property-name='Opslagcapaciteit van SSD'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "storage_disk_type",
            "selector": "[data-property-name='Type harde schijf'] .product-specs__item-spec",
            "type": "text"
        },
        # GPU eigenschappen
        {
            "name": "gpu_chipset",
            "selector": "[data-property-name='Videokaart chipset'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "gpu_type",
            "selector": "[data-property-name='Soort videokaart'] .product-specs__item-spec",
            "type": "text"
        },
        # Besturingssysteem eigenschappen
        {
            "name": "operating_system",
            "selector": "[data-property-name='Besturingssysteem'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "operating_system_language",
            "selector": "[data-property-name='Taal besturingssysteem'] .product-specs__item-spec",
            "type": "text"
        },
        #fysieke eigenschappen
        {
            "name": "model_laptop",
            "selector": "[data-property-name='Model laptop'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "color",
            "selector": "[data-property-name='Kleur'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "material",
            "selector": "[data-property-name='Materiaal'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "height",
            "selector": "[data-property-name='Hoogte'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "width",
            "selector": "[data-property-name='Breedte'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "depth",
            "selector": "[data-property-name='Diepte'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "weight",
            "selector": "[data-property-name='Gewicht'] .product-specs__item-spec",
            "type": "text"
        },
        # wireless
        {
            "name": "mobile_dataconnection",
            "selector": "[data-property-name='Mobiele dataconnectie'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "bluetooth",
            "selector": "[data-property-name='Bluetooth'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "bluetooth_version",
            "selector": "[data-property-name='Bluetooth-versie'] .product-specs__item-spec",
            "type": "text"
        },
        #wired
        {
            "name": "usb_connection",
            "selector": "[data-property-name='Usb-aansluiting'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "amount_of_usb_connections",
            "selector": "[data-property-name='Aantal usb-aansluitingen'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "usb_connection_type",
            "selector": "[data-property-name='Type usb-aansluiting'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "protocol_female_usb_c_port",
            "selector": "[data-property-name='Protocol Female usb-C poort'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "usb_version_female_usb_c_port",
            "selector": "[data-property-name='Usb versie Female usb-C poort'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "video_output_via_usb_c_port",
            "selector": "[data-property-name='Video output via usb C mogelijk'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "amount_of_female_standard_usb_a_ports",
            "selector": "[data-property-name='Aantal female standaard usb-A poorten'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "usb_version_female_standard_usb_a_ports",
            "selector": "[data-property-name='Versie female standaard usb-A poort'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "amount_of_usb_3_1_female_usb_c_ports",
            "selector": "[data-property-name='Aantal usb 3.1 Female usb-C poort'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "hdmi_connection",
            "selector": "[data-property-name='HDMI-aansluiting'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "displayport_connection",
            "selector": "[data-property-name='DisplayPort-aansluiting'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "vga_connection",
            "selector": "[data-property-name='VGA-aansluiting'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "thunderbolt_connection",
            "selector": "[data-property-name='Thunderbolt-aansluiting'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "headphone_jack",
            "selector": "[data-property-name='Hoofdtelefoon aansluiting'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "keyboard_layout",
            "selector": "[data-property-name='Toetsenbordindeling'] .product-specs__item-spec",
            "type": "text"
        },
        # keyboard
        {
            "name": "keyboard_layout",
            "selector": "[data-property-name='Toetsenbordindeling'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "physical_keyboard_layout",
            "selector": "[data-property-name='Fysieke toetsenbordindeling'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "numeric_keyboard",
            "selector": "[data-property-name='Numeriek toetsenblok'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "stain_resistant",
            "selector": "[data-property-name='Morsbestendig'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "keyboard_backlight",
            "selector": "[data-property-name='Verlicht toetsenbord'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "mechanical_keyboard",
            "selector": "[data-property-name='Mechanische toetsen'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "programmable_keys",
            "selector": "[data-property-name='Programmeerbare toetsen'] .product-specs__item-spec",
            "type": "text"
        },
        #audio
        {
            "name": "microphone",
            "selector": "[data-property-name='Ingebouwde microfoon'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "amount_of_speakers",
            "selector": "[data-property-name='Aantal speakers'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "audio_type",
            "selector": "[data-property-name='Geluidsweergave'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "audio_brand",
            "selector": "[data-property-name='brand van ingebouwde computer luidsprekers'] .product-specs__item-spec",
            "type": "text"
        },
        # webcam
        {
            "name": "built_in_camera",
            "selector": "[data-property-name='Ingebouwde camera'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "camera_resolution",
            "selector": "[data-property-name='Beeld-definitie webcams'] .product-specs__item-spec",
            "type": "text"
        },
        # Accu
        {
            "name": "battery_type",
            "selector": "[data-property-name='Accu/batterij technologie'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "battery_capacity",
            "selector": "[data-property-name='Maximale accu/batterijduur'] .product-specs__item-spec",
            "type": "text"
        },
        #fabriek
        {
            "name": "factory_guarantee",
            "selector": "[data-property-name='Fabriekswarranty'] .product-specs__item-spec",
            "type": "text"
        },
        # security
        {
            "name": "TPM",
            "selector": "[data-property-name='TPM (Trusted platform module)'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "kensington_lock",
            "selector": "[data-property-name='Kensington slot'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "windows_hello",
            "selector": "[data-property-name='Windows Hello'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "fingerprint_sensor",
            "selector": "[data-property-name='Vingerafdruk-identiteitssensor'] .product-specs__item-spec",
            "type": "text"
        },
        {
            "name": "security_class",
            "selector": "[data-property-name='Veiligheidsklasse laptops'] .product-specs__item-spec",
            "type": "text"
        },
        #extra
        {
            "name": "amount_of_free_ram_slots",
            "selector": "[data-property-name='Aantal vrije RAM geheugensloten'] .product-specs__item-spec",
            "type": "text"
        },
        #software
        {
            "name": "extra_software",
            "selector": "[data-property-name='Extra geïnstalleerde software'] .product-specs__item-spec",
            "type": "text"
        }
        
    ]
}