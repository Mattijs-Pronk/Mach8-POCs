# persona_data.py

# --- Definities voor Persona-specifieke Data ---
persona_data_store = {
    "student_webdev_docker_budget": {
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Hallo, hoe kan ik je vandaag helpen met het zoeken van een laptop?\n"
                "user: Ik ben een student en ben op zoek naar een laptop voor web development. Ik moet Docker soepel kunnen draaien.\n"
                "assistant: Dat klinkt als een interessante studie! Voor web development is het belangrijk dat je laptop snel en betrouwbaar is, zodat je gemakkelijk kunt werken met verschillende programma's en tools. Neem je de laptop vaak mee naar school?\n"
                "user: Ja ik neem de laptop vaak mee naar school, zou fijn zijn als ik de laptop makkelijk mee kan nemen."
            ),
            "rankingAlgorithm": "category"
        },
        "ground_truth_text": (
            "Voor een student die web development doet, is een laptop nodig met een uitstekende prijs-kwaliteitverhouding (budgetindicatie ~€1000-€1300). "
            "Cruciaal zijn: minimaal 16GB RAM. "
            "Een krachtige, moderne processor (bijv. recente Intel Core i7/Ultra, AMD Ryzen 7, of high-performance ARM) die uitstekende prestaties levert voor veeleisende taken zoals softwareontwikkeling, het draaien van meerdere virtuele machines (zoals Docker containers), en zware multitasking met ontwikkeltools en IDE's. "
            "Een snelle 512GB NVMe SSD (of groter). "
            "Een Full HD (1920x1080) scherm (14-16 inch) is voldoende, helder genoeg voor diverse omgevingen. "
            "Goede batterijduur (idealiter 8+ uur, minimaal 7 uur voor een studiedag). "
            "Draagbaarheid (gewicht onder 2.0 kg, idealiter rond 1.5-1.7 kg). "
            "Goede connectiviteit inclusief meerdere USB-poorten (minimaal één USB-A en één USB-C met data/display/oplaadfunctionaliteit), en HDMI. "
        )
    },
    "professional_datascience_heavy_performance": {
        "api_payload": {
            "category": "Laptop",
            "conversation": [
                {"role": "assistant", "content": "Welkom! Waarmee kan ik u van dienst zijn?"},
                {"role": "user", "content": "Ik zoek een absolute high-end laptop. Ik ben data scientist en train regelmatig zware neurale netwerken en werk met grote datasets. Prestaties en een goed scherm zijn het allerbelangrijkst, budget is minder een issue."},
                {"role": "assistant", "content": "Dat is duidelijk! Een mobiel workstation dus. Heeft u specifieke software-eisen qua besturingssysteem of GPU-voorkeur (NVIDIA CUDA)?"},
                {"role": "user", "content": "Windows Pro en NVIDIA GPU is een must voor CUDA. Minimaal 32GB RAM, liever 64GB."}
            ],
            "rankingAlgorithm": "category"
        },
        "ground_truth_text": (
            "Een professionele data scientist die frequent zware machine learning modellen traint en grote datasets analyseert, vereist een high-performance mobiel workstation. "
            "Absolute vereisten: een high-end Intel Core i7/i9 of AMD Ryzen 7/9 H/HX-serie processor (nieuwste generaties), minimaal 32GB RAM (64GB sterk aanbevolen, upgradebaar), een zeer snelle 1TB NVMe PCIe 4.0 SSD (of groter, eventueel met optie voor een tweede drive), "
            "en een krachtige dedicated NVIDIA GPU (bijv. RTX 4070/A2000 of beter met minimaal 8GB VRAM, geoptimaliseerd voor CUDA). Een scherm met hoge resolutie (minimaal QHD, idealiter 4K OLED) en uitstekende kleurweergave (100% DCI-P3/AdobeRGB) en hoge helderheid is essentieel. "
            "Robuuste bouwkwaliteit (metaal/carbon), effectieve koeling onder zware belasting, een comfortabel toetsenbord met numeriek eiland (indien >15 inch), en uitgebreide connectiviteitsopties (Thunderbolt 4/USB4, meerdere USB-C, SD-kaartlezer, snelle Ethernetpoort) zijn noodzakelijk."
        )
    },
    "freelance_webdev_docker_mobility": {
        "api_payload": {
            "category": "Laptop",
            "conversation": [
                {"role": "assistant", "content": "Hallo, hoe kan ik je vandaag helpen met het zoeken van een laptop?"},
                {"role": "user", "content": "Ik zoek een laptop voor development. Ik ben freelancer."},
                {"role": "assistant", "content": "Interessant! Voor welk type development en heb je specifieke tools die je gebruikt?"},
                {"role": "user", "content": "Voornamelijk websites maken, en ik gebruik Docker veel. Mobiliteit is ook belangrijk, ik werk vaak op locatie."},
                {"role": "assistant", "content": "Oké, webdevelopment met Docker en focus op mobiliteit. Helder!"}
            ],
            "rankingAlgorithm": "category"
        },
        "ground_truth_text": (
            "Voor een freelance webdeveloper die vaak onderweg is en Docker gebruikt, is een balans tussen prestaties, draagbaarheid en batterijduur cruciaal. "
            "Vereisten: een efficiënte maar capabele processor (nieuwere generatie Intel Core i5/i7 U/P-serie of AMD Ryzen 5/7 U/HS-serie, of vergelijkbare ARM), minimaal 16GB RAM (32GB is een plus voor zwaardere Docker setups), een snelle 512GB of 1TB NVMe SSD. "
            "Het scherm moet minimaal Full HD zijn (13-14 inch ideaal voor portabiliteit, 15 inch acceptabel), helder genoeg voor diverse omgevingen (min. 300 nits, 400+ ideaal) en goede kleurdekking (min. 100% sRGB). Een batterijduur van 8+ uur bij normaal gebruik is zeer wenselijk. Gewicht onder 1.5kg is ideaal (max 1.7kg). "
            "Goede en stabiele Wi-Fi (Wi-Fi 6/6E), voldoende poorten (incl. minimaal één USB-C met Power Delivery en DisplayPort-functionaliteit) en een prettig, verlicht toetsenbord zijn belangrijk. Stille werking onder lichte last is een pre."
        )
    }
}