from dotenv import load_dotenv
import os
import json
import pandas as pd
import datetime
import requests
import re
import time # <<< TOEGEVOEGD
from openai import OpenAI
from tqdm import tqdm # For progress bar

load_dotenv()

# Initialize OpenAI client for YOUR custom LLM analysis function
LLM_AVAILABLE = False
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY:
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        LLM_AVAILABLE = True
        print("OpenAI client initialized successfully for custom LLM analysis.")
    except Exception as e:
        print(f"Waarschuwing: Kon OpenAI client niet initialiseren voor custom LLM analysis. LLM-analyse wordt overgeslagen of gebruikt fallback. Fout: {e}")
else:
    print("Waarschuwing: OPENAI_API_KEY niet gevonden in environment. Custom LLM-analyse wordt overgeslagen of gebruikt fallback.")


from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    context_precision,
    context_recall,
)

# --- Definities voor Persona-specifieke Data ---
# persona_data_store = {
#     "student_webdev_docker_budget": {
#         "api_payload": {
#             "category": "Laptop",
#             "conversation": (
#                 "assistant: Hallo, hoe kan ik je vandaag helpen met het zoeken van een laptop?\n"
#                 "user: Hoi! Ik ben een student en ben op zoek naar een laptop voor web development. Ik moet Docker soepel kunnen draaien en ook wat IDE's zoals VS Code.\n"
#                 "assistant: Dat klinkt als een interessante studie! Voor web development en Docker is inderdaad een capabele machine nodig. Neem je de laptop vaak mee naar school of werk je er vooral thuis mee?\n"
#                 "user: Ja, ik neem de laptop dagelijks mee naar school, dus hij moet wel makkelijk mee te nemen zijn. Een goede batterijduur zou ook fijn zijn.\n"
#                 "assistant: Begrepen! Draagbaarheid en batterijduur zijn dus belangrijk. Heb je een budget in gedachten?\n"
#                 "user: Ik hoop iets te vinden rond de 1000-1300 euro."
#             ),
#             "rankingAlgorithm": "conversation"
#         },
#         "ground_truth_text": (
#             "Voor een student die web development doet, is een laptop nodig met een uitstekende prijs-kwaliteitverhouding (budgetindicatie ~€1000-€1300). "
#             "Cruciaal zijn: minimaal 16GB RAM (ideaal voor Docker en IDEs). "
#             "Een krachtige, moderne processor (bijv. recente Intel Core i5/i7 U/P-serie, AMD Ryzen 5/7 U/HS-serie) die goede prestaties levert voor softwareontwikkeling, het draaien van Docker containers, en multitasking. "
#             "Een snelle 512GB NVMe SSD (of groter). "
#             "Een Full HD (1920x1080) scherm (13-15 inch voor draagbaarheid) is voldoende, helder genoeg voor diverse omgevingen. "
#             "Goede batterijduur (idealiter 8+ uur, minimaal 7 uur voor een studiedag). "
#             "Draagbaarheid (gewicht onder 1.8 kg, idealiter rond 1.3-1.6 kg). "
#             "Goede connectiviteit inclusief meerdere USB-poorten (minimaal één USB-A en één USB-C met data/display/oplaadfunctionaliteit), en HDMI. Een prettig toetsenbord is ook belangrijk voor development."
#         )
#     },
#     "general_user_basic_needs": {
#         "api_payload": {
#             "category": "Laptop",
#             "conversation": (
#                 "assistant: Goedendag! Ik help u graag met het vinden van een nieuwe laptop. Kunt u mij vertellen waar u de laptop voornamelijk voor wilt gaan gebruiken?\n"
#                 "user: Hallo, ik zoek een laptop voor thuis. Gewoon voor de e-mail, een beetje op internet surfen, bankzaken regelen, en af en toe een YouTube filmpje kijken. Ik ben niet zo technisch, dus het moet vooral makkelijk werken.\n"
#                 "assistant: Dat is duidelijk. Een laptop voor alledaags gebruik dus. Heeft u een idee van het budget dat u in gedachten heeft?\n"
#                 "user: Nou, ik dacht aan iets tussen de 500 en 700 euro, als dat mogelijk is. Het hoeft niet het allernieuwste te zijn, als het maar goed werkt.\n"
#                 "assistant: Prima, binnen dat budget zijn er zeker goede opties. Is er een bepaalde schermgrootte die u prettig vindt, of heeft u daar geen specifieke voorkeur voor? En is het belangrijk dat de laptop licht is om mee te nemen, of gebruikt u hem voornamelijk op één plek?\n"
#                 "user: Een normaal scherm is prima, niet te klein. Ik gebruik hem eigenlijk alleen thuis op de bank of aan de eettafel, dus hij hoeft niet superlicht te zijn."
#             ),
#             "rankingAlgorithm": "conversation"
#         },
#         "ground_truth_text": (
#             "Voor een gebruiker die een laptop zoekt voor alledaagse taken zoals internetten, e-mailen, en media consumptie, en die minder technisch onderlegd is, is een betrouwbare en gebruiksvriendelijke laptop belangrijk. Budgetindicatie ~€500-€700. "
#             "Specificaties: Een moderne Intel Core i3 (of AMD Ryzen 3) is vaak al voldoende, een Core i5 (of Ryzen 5) biedt meer comfort voor de toekomst. Minimaal 8GB RAM is essentieel. "
#             "Een snelle SSD (Solid State Drive) van minimaal 256GB (512GB aanbevolen voor meer opslagruimte) is cruciaal voor een vlotte gebruikerservaring. "
#             "Een Full HD (1920x1080) scherm van circa 15.6 inch (of 14 inch als iets compacter wenselijk is) met IPS-paneel voor goede kijkhoeken en redelijke helderheid is prettig. "
#             "Een batterijduur van minimaal 5-6 uur bij licht gebruik is voldoende voor thuisgebruik. Gewicht is minder kritisch. "
#             "Voldoende poorten zoals USB-A, USB-C, en HDMI zijn handig. Een comfortabel toetsenbord en een nauwkeurige touchpad. "
#             "Windows Home editie, idealiter met minimale bloatware."
#         )
#     },
#     "gamer_high_performance": { 
#         "api_payload": {
#             "category": "Laptop",
#             "conversation": (
#                 "assistant: Hey! Op zoek naar een serieuze gaming laptop? Wat voor games speel je voornamelijk en wat zijn je verwachtingen?\n"
#                 "user: Yo! Inderdaad. Ik wil de nieuwste AAA-titels zoals Cyberpunk 2077 met ray tracing, en competitieve shooters zoals Valorant op hoge framerates kunnen spelen. Het beeld moet super vloeiend zijn.\n"
#                 "assistant: Nice! Dan kijken we naar de topmodellen. Heb je een budget in gedachten? En hoe belangrijk is draagbaarheid versus pure kracht en koeling?\n"
#                 "user: Budget is rond de 2000 tot 2500 euro. Performance en goede koeling zijn het allerbelangrijkst, hij hoeft niet superlicht te zijn. Een 16 of 17 inch scherm met hoge refresh rate (minimaal 165Hz) en QHD resolutie is een must.\n"
#                 "assistant: Helder. QHD met hoge refresh rate. Zijn er nog specifieke features die je belangrijk vindt? Denk aan toetsenbordverlichting, specifieke poorten, of misschien een voorkeur voor NVIDIA of AMD GPUs?\n"
#                 "user: Een goed mechanisch-voelend toetsenbord met RGB is wel vet. NVIDIA GPU heeft mijn voorkeur vanwege DLSS. En genoeg USB-poorten voor m'n gear. Oh, en Wi-Fi 6E zou top zijn.\n"
#                 "assistant: Top, dat geeft een goed beeld. We gaan op zoek naar een beest met een NVIDIA GPU, QHD 165Hz+ scherm, goed toetsenbord en de juiste connectiviteit binnen je budget!"
#             ),
#             "rankingAlgorithm": "conversation"
#         },
#         "ground_truth_text": (
#             "Voor een hardcore gamer die de nieuwste AAA-titels op hoge tot ultra grafische instellingen (inclusief ray tracing) wil spelen en hoge framerates in competitieve games eist. Budgetindicatie ~€2000-€2500+. "
#             "Cruciale specificaties: Een high-end, recente generatie Intel Core i7/i9 H/HX-serie processor of AMD Ryzen 7/9 H/HX-serie processor. "
#             "Minimaal 16GB DDR5 RAM (32GB sterk aanbevolen voor veeleisende games en toekomstbestendigheid). "
#             "Een snelle NVMe PCIe 4.0 SSD van minimaal 1TB, idealiter met ruimte voor een tweede SSD. "
#             "Een krachtige NVIDIA GeForce RTX GPU, minimaal RTX 4070 (laptop), idealiter RTX 4080 (laptop) voor QHD gaming met hoge settings en ray tracing. Voldoende VRAM (minimaal 8GB, 12GB+ voor 4080). "
#             "Een scherm van 16 of 17 inch met QHD (2560x1440/1600) resolutie, hoge verversingssnelheid (minimaal 165Hz, 240Hz is beter voor competitief), lage responstijd (<3ms GtG), en ondersteuning voor G-Sync/Adaptive Sync. Goede kleurdekking (DCI-P3) en hoge helderheid (350+ nits). "
#             "Een geavanceerd en effectief koelsysteem is absoluut noodzakelijk. "
#             "Een responsief toetsenbord met N-key rollover, goede travel, en (per-key) RGB-verlichting. "
#             "Uitgebreide connectiviteit: Wi-Fi 6E, 2.5Gbps Ethernetpoort, Thunderbolt 4 / USB4 (indien Intel), meerdere snelle USB-A en USB-C poorten (waarvan één met DisplayPort alt-mode), en HDMI 2.1."
#         )
#     }
# }

persona_data_store = {
    "general_user_basic_needs": {
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Goedendag! Ik help u graag met het vinden van een nieuwe laptop. Kunt u mij vertellen waar u de laptop voornamelijk voor wilt gaan gebruiken?\n"
                "user: Hallo, ik zoek een laptop voor thuis. Gewoon voor de e-mail, een beetje op internet surfen, bankzaken regelen, en af en toe een YouTube filmpje kijken. Ik ben niet zo technisch, dus het moet vooral makkelijk werken.\n"
                "assistant: Dat is duidelijk. Een laptop voor alledaags gebruik dus. Heeft u een idee van het budget dat u in gedachten heeft?\n"
                "user: Nou, ik dacht aan iets tussen de 500 en 700 euro, als dat mogelijk is. Het hoeft niet het allernieuwste te zijn, als het maar goed werkt.\n"
                "assistant: Prima, binnen dat budget zijn er zeker goede opties. Is er een bepaalde schermgrootte die u prettig vindt, of heeft u daar geen specifieke voorkeur voor? En is het belangrijk dat de laptop licht is om mee te nemen, of gebruikt u hem voornamelijk op één plek?\n"
                "user: Een normaal scherm is prima, niet te klein. Ik gebruik hem eigenlijk alleen thuis op de bank of aan de eettafel, dus hij hoeft niet superlicht te zijn."
            ),
            "rankingAlgorithm": "conversation"
        },
        "ground_truth_text": (
            "Voor een gebruiker die een laptop zoekt voor alledaagse taken zoals internetten, e-mailen, en media consumptie, en die minder technisch onderlegd is, is een betrouwbare en gebruiksvriendelijke laptop belangrijk. Budgetindicatie ~€500-€700. "
            "Specificaties: Een moderne Intel Core i3 (of AMD Ryzen 3) is vaak al voldoende, een Core i5 (of Ryzen 5) biedt meer comfort voor de toekomst. Minimaal 8GB RAM is essentieel. "
            "Een snelle SSD (Solid State Drive) van minimaal 256GB (512GB aanbevolen voor meer opslagruimte) is cruciaal voor een vlotte gebruikerservaring. "
            "Een Full HD (1920x1080) scherm van circa 15.6 inch (of 14 inch als iets compacter wenselijk is) met IPS-paneel voor goede kijkhoeken en redelijke helderheid is prettig. "
            "Een batterijduur van minimaal 5-6 uur bij licht gebruik is voldoende voor thuisgebruik. Gewicht is minder kritisch. "
            "Voldoende poorten zoals USB-A, USB-C, en HDMI zijn handig. Een comfortabel toetsenbord en een nauwkeurige touchpad. "
            "Windows Home editie, idealiter met minimale bloatware."
        )
    },
    "student_budget_portability": {
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Hallo! Waarmee kan ik je helpen bij het vinden van een nieuwe laptop?\n"
                "user: Hoi, ik ben student en zoek een laptop voor school. Vooral voor aantekeningen maken, verslagen typen en online research. Hij moet niet te zwaar zijn, want ik neem 'm elke dag mee.\n"
                "assistant: Begrijpelijk, een lichte en handzame laptop is dan fijn. Heb je een budget in gedachten?\n"
                "user: Ja, ik hoop iets te vinden onder de 600 euro. En hij moet wel een beetje snel opstarten en niet vastlopen als ik een paar programma's open heb.\n"
                "assistant: Duidelijk. En qua batterij, is het belangrijk dat die een hele collegedag meegaat?\n"
                "user: Dat zou wel ideaal zijn, ja. Of in ieder geval lang genoeg zodat ik niet steeds een stopcontact hoef te zoeken."
            ),
            "rankingAlgorithm": "conversation"
        },
        "ground_truth_text": (
            "Voor een student die een betaalbare en draagbare laptop zoekt voor studiegerelateerde taken, is een goede balans tussen prijs, gewicht en accuduur belangrijk. Budgetindicatie tot €600."
            "Specificaties: Een recente Intel Core i3/i5 (of AMD Ryzen 3/5) is geschikt. Minimaal 8GB RAM (16GB is een plus voor soepeler multitasken)."
            "Een SSD van minimaal 256GB voor snelle opstarttijden en programma's."
            "Een scherm van 13 tot 14 inch is ideaal voor portabiliteit, Full HD (1920x1080) resolutie."
            "Een accuduur van minimaal 7-8 uur bij licht gebruik is wenselijk. Gewicht idealiter onder de 1.5 kg."
            "Voldoende USB-poorten (mix van USB-A en USB-C is handig). Een degelijk toetsenbord is essentieel voor typwerk."
        )
    },
    "senior_ease_of_use_communication": {
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Goedemiddag, ik help u graag. Voor wie en waarvoor zoekt u een laptop?\n"
                "user: Ik zoek een laptop voor mijn moeder van 75. Ze wil graag makkelijk kunnen videobellen met de kleinkinderen, e-mailen en af en toe het nieuws lezen of een spelletje zoals patience doen. Het moet vooral niet te ingewikkeld zijn.\n"
                "assistant: Dat klinkt als een mooi doel. Gebruiksgemak is dus de prioriteit. Heeft u een budget in gedachten?\n"
                "user: Rond de 500, misschien 600 euro. Een duidelijk en misschien wat groter scherm zou fijn zijn voor haar ogen.\n"
                "assistant: Dat is een goed uitgangspunt. Moet de laptop makkelijk te verplaatsen zijn, of blijft hij meestal op één plek?\n"
                "user: Hij blijft meestal thuis, dus het gewicht is niet zo belangrijk. Een goed toetsenbord met duidelijke letters wel."
            ),
            "rankingAlgorithm": "conversation"
        },
        "ground_truth_text": (
            "Voor een senior die een zeer gebruiksvriendelijke laptop zoekt voor communicatie (videobellen, e-mail) en lichte ontspanning, is eenvoud en een helder display cruciaal. Budgetindicatie ~€500-€600. "
            "Specificaties: Een Intel Core i3 (of AMD Ryzen 3) of zelfs een moderne Pentium/Celeron kan volstaan. 8GB RAM is aanbevolen voor een soepele ervaring. "
            "Opslag van minimaal 128GB of meer"
            "Een 15 inch (of groter) Full HD scherm met goede helderheid en contrast, bij voorkeur IPS. Mogelijk instellingen voor grotere tekst/iconen. "
            "Een degelijke webcam en microfoon zijn belangrijk voor videobellen. Een comfortabel toetsenbord met duidelijke, goed leesbare toetsen. "
            "Voldoende USB-poorten voor muis of andere accessoires. "
        )
    },
    "home_office_light_creative": {
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Welkom! Vertel eens, wat voor laptop zoek je en wat wil je ermee gaan doen?\n"
                "user: Ik werk sinds kort vaker thuis en zoek een laptop voor mijn administratie, e-mail, en videovergaderingen. Daarnaast vind ik het leuk om in mijn vrije tijd foto's te bewerken, maar niet super professioneel, gewoon voor de hobby.\n"
                "assistant: Oké, een laptop voor productiviteit met een beetje extra voor creatieve hobby's. Wat is je budget ongeveer?\n"
                "user: Ik dacht aan maximaal 800 euro. Hij hoeft niet per se heel licht te zijn, maar een goed scherm voor die fotobewerking is wel een pre.\n"
                "assistant: Dat is een mooi budget. En heb je voorkeur voor een bepaalde schermgrootte?\n"
                "user: Rond de 15 inch lijkt me prima. En voldoende opslag voor mijn documenten en foto's is ook handig."
            ),
            "rankingAlgorithm": "conversation"
        },
        "ground_truth_text": (
            "Voor een thuiswerker die ook lichte creatieve taken (fotobewerking) uitvoert, is een laptop met een goed scherm en redelijke prestaties belangrijk. Budgetindicatie tot €800. "
            "Specificaties: Een moderne Intel Core i5/i7 (of AMD Ryzen 5/7) is een goede keuze. Minimaal 8GB RAM, maar 16GB is sterk aanbevolen voor soepelere fotobewerking en multitasking. "
            "Een snelle SSD van minimaal 512GB voor het besturingssysteem, programma's en opslag van foto's."
            "Een 15 inch Full HD IPS-scherm met goede kleurweergave en helderheid. "
            "Een degelijke webcam en microfoon voor videovergaderingen. Voldoende poorten, inclusief HDMI voor een extern scherm en USB-C. "
            "Accuduur is minder kritisch als hij voornamelijk thuis gebruikt wordt, maar 5-6 uur is een nette basis."
        )
    },
    "family_shared_entertainment": {
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Goedendag! Op zoek naar een nieuwe laptop? Waar gaat u hem voornamelijk voor gebruiken?\n"
                "user: Ja, we zoeken een laptop voor het gezin. De kinderen moeten er huiswerk op kunnen maken, en we willen er films en series op kunnen kijken. Misschien af en toe een simpel spelletje, maar geen zware dingen.\n"
                "assistant: Een familielaptop dus, voor uiteenlopende taken. Heeft u een budget in gedachten?\n"
                "user: Liefst niet veel meer dan 700 euro. Hij moet wel een beetje tegen een stootje kunnen, met kinderen in huis.\n"
                "assistant: Dat is een goed punt. En qua schermgrootte, heeft u daar een voorkeur voor? Moet hij makkelijk verplaatst worden in huis?\n"
                "user: Een redelijk groot scherm zou fijn zijn voor films, zeg 15 of 16 inch. Hij wordt wel in huis verplaatst, maar hoeft niet superlicht te zijn."
            ),
            "rankingAlgorithm": "conversation"
        },
        "ground_truth_text": (
            "Voor een gezin dat een laptop deelt voor huiswerk, media consumptie en lichte spelletjes, is een robuuste allrounder met een goed scherm wenselijk. Budgetindicatie tot €700. "
            "Specificaties: Een recente Intel Core i3/i5 (of AMD Ryzen 3/5) biedt voldoende kracht. 8GB RAM is minimaal, 16GB is prettig voor de toekomst en meerdere gebruikers. "
            "Een SSD van 512GB wordt aanbevolen voor opslag van documenten, media en een paar spelletjes. "
            "Een 15 inch (of groter) Full HD IPS-scherm voor goede kijkhoeken en prettige filmweergave. "
            "Goede speakers of de mogelijkheid om eenvoudig externe speakers/koptelefoon aan te sluiten. "
            "Een stevige bouwkwaliteit is een pluspunt. Voldoende USB-poorten voor verschillende apparaten. "
        )
    },
    "young_professional_on_the_go": {
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Hallo, ik help je graag met een nieuwe laptop. Wat zijn je belangrijkste activiteiten?\n"
                "user: Ik ben net begonnen met werken en reis best veel voor m'n baan, ook naar klanten. Ik heb een laptop nodig die makkelijk mee te nemen is, er professioneel uitziet en een goede batterij heeft. Vooral voor presentaties, e-mail en documenten.\n"
                "assistant: Klinkt goed. Een lichte, representatieve laptop met lange accuduur dus. Wat is je budget ongeveer?\n"
                "user: Ik denk tot zo'n 900 euro. Hij moet wel vlot werken, ik wil niet wachten als ik snel iets moet laten zien.\n"
                "assistant: Begrijpelijk. En is er een voorkeur voor schermgrootte, of is vooral het gewicht en de batterij belangrijk?\n"
                "user: Liever niet te groot, 13 of 14 inch is prima. Gewicht en batterij zijn inderdaad het belangrijkst."
            ),
            "rankingAlgorithm": "conversation"
        },
        "ground_truth_text": (
            "Voor een jonge professional die veel onderweg is, is een lichte, slanke laptop met een lange accuduur en professionele uitstraling essentieel. Budgetindicatie €700-€900. "
            "Specificaties: Een moderne, energiezuinige Intel Core i5/i7 (of AMD Ryzen 5/7) is ideaal. Minimaal 8GB RAM, 16GB voor soepeler multitasken. "
            "Een snelle SSD van 256GB of 512GB. "
            "Een 13 of 14 inch Full HD IPS-scherm met goede helderheid. "
            "Accuduur van minimaal 8-10 uur bij licht gebruik. Gewicht idealiter onder 1.4 kg. "
            "Goede connectiviteit (USB-C met Thunderbolt is een plus, HDMI). Een comfortabel toetsenbord en een goede webcam/microfoon voor online meetings. "
        )
    },
    "aspiring_writer_blogger": {
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Goedendag, wat voor laptop zoekt u precies?\n"
                "user: Ik wil graag meer gaan schrijven, misschien een blog beginnen. Ik zoek een laptop met een heel fijn toetsenbord, want ik ga er veel op typen. Een goed leesbaar scherm is ook belangrijk.\n"
                "assistant: Een laptop gericht op schrijfcomfort dus. Heeft u een budget in gedachten?\n"
                "user: Ja, zo rond de 600 tot 800 euro. Hij hoeft niet superkrachtig te zijn, maar wel prettig werken voor lange sessies.\n"
                "assistant: En is het belangrijk dat de laptop makkelijk mee te nemen is, of gebruikt u hem vooral thuis?\n"
                "user: Een beetje van beide, maar het toetsenbord en scherm zijn echt prioriteit. Een redelijke batterij is ook fijn."
            ),
            "rankingAlgorithm": "conversation"
        },
        "ground_truth_text": (
            "Voor een aspirant schrijver of blogger is een laptop met een uitstekend toetsenbord en een prettig, helder scherm cruciaal voor productiviteit en comfort. Budgetindicatie €600-€800. "
            "Specificaties: Een Intel Core i3/i5 (of AMD Ryzen 3/5) is voldoende. 8GB RAM is prima, 16GB biedt meer comfort. "
            "Een opslag van 512GB of meer. "
            "Een 14 of 15 inch Full HD IPS-scherm met goede helderheid en eventueel een matte afwerking om reflecties te verminderen. "
            "Focus op modellen die bekend staan om hun toetsenbordkwaliteit (goede travel, feedback). Accuduur van 6-8 uur. "
            "Gewicht is secundair, maar onder 1.8kg is prettig als hij af en toe meegenomen wordt. Voldoende USB-poorten. "
        )
    },
    "hobbyist_photographer_basic_editing": {
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Hallo! Ik help u graag met het vinden van een laptop. Waar wilt u de laptop voornamelijk voor gebruiken?\n"
                "user: Ik fotografeer graag als hobby en wil mijn foto's kunnen bekijken en een beetje bewerken. Geen super ingewikkelde dingen, maar wel dat de kleuren goed zijn. En ik heb aardig wat foto's, dus opslag is ook wel een ding.\n"
                "assistant: Een laptop voor fotobewerking op hobbyniveau dus, met aandacht voor kleurechtheid en opslag. Wat is uw budget?\n"
                "user: Ik dacht aan iets tussen de 700 en 1000 euro. Hij hoeft niet het allersnelste te zijn, maar wel soepel werken met fotoprogramma's.\n"
                "assistant: Duidelijk. En is draagbaarheid belangrijk, of gebruikt u hem vooral thuis?\n"
                "user: Vooral thuis, dus een wat groter, goed scherm is belangrijker dan gewicht."
            ),
            "rankingAlgorithm": "conversation"
        },
        "ground_truth_text": (
            "Voor een hobbyfotograaf die basis fotobewerking doet, is een laptop met een kleurecht scherm en voldoende opslag en rekenkracht belangrijk. Budgetindicatie €700-€1000. "
            "Specificaties: Een Intel Core i5/i7 (of AMD Ryzen 5/7) is een goed startpunt. Minimaal 16GB RAM is sterk aanbevolen. "
            "Een snelle SSD van minimaal 512GB. "
            "Een 15 inch Full HD IPS-scherm met goede kleurdekking en helderheid. "
            "Een aparte (dedicated) grafische kaart op instapniveau (bijv. NVIDIA MX-serie, basis RTX/Radeon of intel Arc) kan helpen, maar is niet strikt noodzakelijk voor basisbewerking. "
            "Voldoende USB-poorten voor kaartlezers en externe schijven, HDMI-poort. "
        )
    },
    "online_course_taker_adult_learner": {
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Goedendag, ik help u graag een passende laptop te vinden. Wat wilt u er hoofdzakelijk mee doen?\n"
                "user: Ik volg een online cursus en heb een simpele laptop nodig om de lessen te volgen, aantekeningen te maken en opdrachten in te leveren. Het hoeft niet duur te zijn.\n"
                "assistant: Een betaalbare laptop voor studeren dus. Wat is uw budget ongeveer?\n"
                "user: Het liefst onder de 500 euro, als dat kan. Hij moet wel gewoon internet en tekstverwerking aankunnen.\n"
                "assistant: Dat moet lukken. Is er een voorkeur voor schermgrootte of gewicht?\n"
                "user: Niet echt, als ik de lessen maar goed kan zien. Een goede webcam zou wel handig zijn voor interactieve sessies."
            ),
            "rankingAlgorithm": "conversation"
        },
        "ground_truth_text": (
            "Voor een volwassen cursist die online leert, is een betrouwbare en betaalbare laptop voor basistaken zoals videostreaming, tekstverwerking en internetgebruik voldoende. Budgetindicatie tot €500. "
            "Specificaties: Een moderne Intel Core i3/i5, Pentium, Celeron (of AMD Athlon/Ryzen 3/5) kan volstaan. Minimaal 4GB RAM, maar 8GB wordt sterk aanbevolen voor een soepelere ervaring. "
            "Een opslag van 128GB of 256GB. "
            "Een 14 of 15 inch scherm, HD of Full HD resolutie. "
            "Een degelijke webcam en microfoon. Goede Wi-Fi verbinding. Accuduur van 5-6 uur. "
            "Voldoende USB-poorten."
        )
    },
    "travel_enthusiast_media_planning": {
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Hallo! Op zoek naar een laptop? Voor welk doel voornamelijk?\n"
                "user: Ik reis veel en zoek een kleine, lichte laptop. Vooral om onderweg films te kijken, mijn reis te plannen, en contact te houden. Een lange batterijduur is dus heel belangrijk.\n"
                "assistant: Een echte reisgenoot dus! Wat is je budget ongeveer?\n"
                "user: Rond de 500 à 750 euro. Hij hoeft niet superkrachtig te zijn, maar wel stevig genoeg voor in een rugzak.\n"
                "assistant: En qua schermgrootte, denk je aan iets heel compacts?\n"
                "user: Ja, 13 inch of kleiner als dat kan, zolang het maar niet te priegelig wordt om een film op te kijken."
            ),
            "rankingAlgorithm": "conversation"
        },
        "ground_truth_text": (
            "Voor een reisliefhebber is een compacte, lichte laptop met een zeer goede accuduur en degelijke bouwkwaliteit ideaal voor media consumptie en reisplanning. Budgetindicatie €500-€750. "
            "Specificaties: Een energiezuinige processor (Intel Core i3/i5 U-serie, of vergelijkbare AMD). 8GB RAM. "
            "Een opslag van minimaal 512GB. "
            "Een 11 tot 13 inch scherm, Full HD indien mogelijk voor kijkplezier. "
            "Accuduur van 10+ uur is zeer wenselijk. Gewicht onder 1.3 kg. "
            "Stevige behuizing. Goede Wi-Fi. Voldoende USB-poorten, eventueel USB-C voor opladen. "
        )
    },
    "small_business_owner_admin_marketing": {
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Goedendag! Waarmee kan ik u helpen bij uw laptopkeuze?\n"
                "user: Ik heb een klein bedrijfje en zoek een betrouwbare laptop voor de administratie, e-mail, facturatie en af en toe wat simpele marketing dingen maken, zoals social media posts. Hij moet vooral stabiel zijn.\n"
                "assistant: Een werkpaard voor uw bedrijf dus. Heeft u een budget in gedachten?\n"
                "user: Ik dacht aan iets tot 850 euro. Een numeriek toetsenblok zou handig zijn voor de boekhouding.\n"
                "assistant: Goed punt. En is het belangrijk dat hij makkelijk mee te nemen is, of werkt u vooral op één locatie?\n"
                "user: Vooral op kantoor. Een goede, snelle internetverbinding is ook belangrijk."
            ),
            "rankingAlgorithm": "conversation"
        },
        "ground_truth_text": (
            "Voor een kleine ondernemer die een laptop nodig heeft voor administratie, communicatie en lichte marketing, is betrouwbaarheid en efficiëntie key. Budgetindicatie tot €850. "
            "Specificaties: Een Intel Core i5 (of AMD Ryzen 5). Minimaal 8GB RAM, 16GB voor meer comfort. "
            "Een snelle SSD van 512GB. "
            "Een 15 inch Full HD scherm."
            "Goede connectiviteit: stabiele Wi-Fi, Ethernetpoort is een plus, voldoende USB-poorten, HDMI. "
            "Een comfortabel toetsenbord. Een degelijke webcam voor eventuele klantgesprekken. "
        )
    },
    "teenager_school_light_gaming_streaming": {
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Hoi! Op zoek naar een laptop? Vertel eens wat je ermee wilt doen.\n"
                "user: Ik zit op de middelbare school en heb een laptop nodig voor huiswerk en presentaties. Maar ik wil er ook wel een beetje op kunnen gamen, niet de allernieuwste spellen, maar wel dingen zoals Minecraft of Fortnite. En natuurlijk Netflix kijken.\n"
                "assistant: Een allround laptop voor school en ontspanning dus. Wat is je budget ongeveer?\n"
                "user: Mijn ouders willen tot ongeveer 800 euro uitgeven. Hij moet wel snel genoeg zijn voor die spellen.\n"
                "assistant: Oké. En is gewicht belangrijk, of een lange batterijduur?\n"
                "user: Batterij voor school zou handig zijn. Gewicht niet super belangrijk, hij gaat wel in m'n tas."
            ),
            "rankingAlgorithm": "conversation"
        },
        "ground_truth_text": (
            "Voor een tiener die een laptop zoekt voor schoolwerk, streaming en lichte gaming, is een goede balans tussen prestaties, een degelijk scherm en accuduur nodig. Budgetindicatie tot €800. "
            "Specificaties: Een Intel Core i5/i7 (of AMD Ryzen 5/7) met geïntegreerde graphics die redelijk presteren (Iris Xe, Radeon Vega) of een instapmodel dedicated videokaart (bijv. NVIDIA MX-serie, GTX 1650, basis RTX of intel Arc). Minimaal 8GB RAM, 16GB is beter voor gaming. "
            "Een SSD van 512GB. "
            "Een 15 inch Full HD scherm, eventueel met een hogere verversingssnelheid. "
            "Accuduur van 6-7 uur voor schooldagen. "
        )
    },
    "retiree_hobby_learning_connectivity": {
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Goedemiddag, ik help u graag met een nieuwe laptop. Wat zijn uw wensen?\n"
                "user: Ik ben met pensioen en wil graag een laptop om nieuwe dingen te leren online, zoals een taalcursus of stamboomonderzoek. Ook voor contact met vrienden en familie en het nieuws bijhouden.\n"
                "assistant: Dat klinkt als een mooie invulling! Gebruiksgemak is vast belangrijk. Heeft u een budget?\n"
                "user: Ja, zo rond de 600 euro. Het hoeft niet ingewikkeld te zijn en een helder scherm zou fijn zijn.\n"
                "assistant: Duidelijk. En gebruikt u de laptop voornamelijk thuis?\n"
                "user: Ja, eigenlijk altijd thuis."
            ),
            "rankingAlgorithm": "conversation"
        },
        "ground_truth_text": (
            "Voor een gepensioneerde die actief online wil leren en verbonden wil blijven, is een gebruiksvriendelijke laptop met een helder scherm en betrouwbare prestaties voor alledaagse taken geschikt. Budgetindicatie ~€500-€700. "
            "Specificaties: Een Intel Core i3/i5 (of AMD Ryzen 3/5), 8GB RAM. "
            "Een opslag van 256GB of 512GB. "
            "Een 15 inch Full HD IPS-scherm voor goede leesbaarheid en kijkhoeken. "
            "Een comfortabel toetsenbord en een goede webcam/microfoon. "
            "Voldoende USB-poorten. "
        )
    },
    "second_laptop_kitchen_quick_lookups": {
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Hallo, u zoekt een laptop. Waarvoor gaat u deze voornamelijk gebruiken?\n"
                "user: Ik zoek eigenlijk een goedkope, simpele laptop voor in de keuken. Om recepten op te zoeken, even snel het weer te checken of muziek te luisteren tijdens het koken. Echt geen zware taken.\n"
                "assistant: Een handige keukenhulp dus! Wat is uw maximale budget?\n"
                "user: Liefst onder de 400 euro. Hij moet wel makkelijk schoon te maken zijn, haha, grapje... nou ja, niet te kwetsbaar.\n"
                "assistant: Ik begrijp het. Compact en betaalbaar. Schermgrootte nog een voorkeur?\n"
                "user: Niet te groot, 11 tot 14 inch is prima. En hij moet snel opstarten voor die snelle zoekacties."
            ),
            "rankingAlgorithm": "conversation"
        },
        "ground_truth_text": (
            "Voor een tweede laptop bedoeld voor snelle lookups en basisgebruik in bijvoorbeeld de keuken, is een compacte, betaalbare en snel opstartende laptop ideaal. Budgetindicatie tot €400. "
            "Specificaties: Een instapmodel processor (Intel Celeron/Pentium, AMD Athlon). 4GB RAM (8GB is een plus als het binnen budget past). "
            "Een eMMC of kleine SSD (64GB of 128GB) voor snelle opstarttijden. Opslag is minder kritisch voor dit doel. "
            "Een 11 tot 14 inch scherm, HD-resolutie is acceptabel, Full HD is beter. "
            "ChromeOS is zeer geschikt vanwege snelheid, eenvoud en prijs. "
            "Redelijke accuduur (5+ uur). Eventueel een model met een wat robuustere bouw of makkelijk afneembare oppervlakken."
        )
    },
    "teacher_presentations_classroom_management": {
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Goedendag! Waarmee kan ik u van dienst zijn voor een nieuwe laptop?\n"
                "user: Ik ben leraar en heb een laptop nodig die ik makkelijk kan meenemen tussen klassen. Vooral voor het geven van presentaties, het bijhouden van cijfers en communicatie met ouders en leerlingen.\n"
                "assistant: Een draagbare en betrouwbare partner voor in het onderwijs dus. Wat is uw budget ongeveer?\n"
                "user: Ik hoop iets te vinden rond de 700 euro. Hij moet wel goed kunnen verbinden met beamers en digiborden.\n"
                "assistant: Dat is een belangrijk punt. Heeft u voorkeur voor een bepaalde schermgrootte of accuduur?\n"
                "user: 14 inch is denk ik een goede balans. En een batterij die een schooldag meegaat zou top zijn."
            ),
            "rankingAlgorithm": "conversation"
        },
        "ground_truth_text": (
            "Voor een docent die een laptop nodig heeft voor presentaties, administratie en communicatie, is een draagbare, betrouwbare laptop met goede connectiviteit en accuduur essentieel. Budgetindicatie ~€600-€800. "
            "Specificaties: Een Intel Core i3/i5 (of AMD Ryzen 3/5). 8GB RAM (16GB is comfortabeler). "
            "Een opslag van 256GB of 512GB. "
            "Een 14 inch Full HD scherm. Gewicht onder 1.6 kg. "
            "Goede accuduur (minimaal 7-8 uur). "
            "Belangrijk: HDMI-poort en voldoende USB-poorten (USB-A en USB-C) voor aansluiten op projectoren, digiborden en andere randapparatuur. "
            "Een goede webcam en microfoon. Comfortabel toetsenbord. "
        )
    },
    "casual_gamer_indie_older_titles": { 
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Hallo, op zoek naar een gaming laptop?\n"
                "user: Nou ja, niet echt een hardcore gaming laptop. Ik speel graag wat oudere spellen of indie games, geen super zware grafische dingen. En ik gebruik hem ook voor internet en films.\n"
                "assistant: Een allround laptop met wat extra grafische pit voor casual gaming dus. Wat is je budget?\n"
                "user: Rond de 800 à 900 euro. Hij hoeft niet het dunste of lichtste te zijn, als de spellen maar soepel draaien.\n"
                "assistant: Begrijpelijk. Wat voor schermgroote ben je naar op zoek?\n"
                "user: 15 inch is prima. En voldoende opslag voor een paar spellen is wel handig."
            ),
            "rankingAlgorithm": "conversation"
        },
        "ground_truth_text": (
            "Voor een casual gamer die oudere titels en indie games speelt, is een laptop met een capabele (maar niet high-end) grafische kaart en een goede processor belangrijk. Budgetindicatie €700-€900. "
            "Specificaties: Een Intel Core i5/i7 (of AMD Ryzen 5/7). 16GB RAM wordt aanbevolen voor gaming. "
            "Een SSD van 512GB (of groter). "
            "Een 15 inch Full HD scherm. Een dedicated grafische kaart op instap- tot middenniveau (bijv. NVIDIA GeForce GTX 1650/1650Ti, RTX 3050, of vergelijkbare AMD Radeon of vergelijkbaar Intel model). "
            "Degelijke koeling is een plus voor langere gamesessies. "
        )
    },
    "user_mild_visual_impairment": {
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Goedemiddag. Ik help u graag met het kiezen van een laptop. Zijn er specifieke wensen?\n"
                "user: Ja, ik zie niet meer zo heel goed. Ik zoek een laptop met een groot, duidelijk scherm. En het toetsenbord moet ook goed leesbaar zijn. Ik gebruik hem voor e-mail, internet en wat tekstverwerken.\n"
                "assistant: Dat is een duidelijke behoefte. Een laptop met focus op leesbaarheid dus. Wat is uw budget?\n"
                "user: Ongeveer 600 tot 800 euro. Hij hoeft niet super snel te zijn, maar wel makkelijk in gebruik.\n"
                "assistant: En gebruikt u de laptop voornamelijk op één plek?\n"
                "user: Ja, thuis."
            ),
            "rankingAlgorithm": "conversation"
        },
        "ground_truth_text": (
            "Voor een gebruiker met een milde visuele beperking is een laptop met een groot, helder scherm met goed contrast en een duidelijk leesbaar toetsenbord essentieel. Budgetindicatie €600-€800. "
            "Specificaties: Een Intel Core i3/i5 (of AMD Ryzen 3/5). 8GB RAM. "
            "Een SSD van 256GB of 512GB. "
            "Een 15 inch of bij voorkeur 17 inch Full HD IPS-scherm met goede helderheid en contrast. Overweeg modellen met matte schermen om reflecties te minimaliseren. "
            "Een toetsenbord met duidelijke, grote letters, bij voorkeur met achtergrondverlichting. "
            "Voldoende USB-poorten voor eventuele externe hulpmiddelen."
        )
    },
    "parent_buying_first_laptop_young_child": {
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Hallo! Op zoek naar een laptop voor uw kind?\n"
                "user: Ja, voor mijn dochter van 8. Haar eerste laptop. Vooral voor schoolwerk, educatieve spelletjes en misschien wat YouTube Kids. Hij moet wel tegen een stootje kunnen en niet te duur zijn.\n"
                "assistant: Een kindvriendelijke en robuuste laptop dus. Wat is het budget ongeveer?\n"
                "user: Liefst onder de 450 euro. En makkelijk voor haar om te gebruiken.\n"
                "assistant: Duidelijk. En is er een voorkeur voor grootte of gewicht?\n"
                "user: Niet te groot, misschien 11 of 13 inch. En niet te zwaar, zodat ze hem zelf kan pakken."
            ),
            "rankingAlgorithm": "conversation"
        },
        "ground_truth_text": (
            "Voor een jong kind als eerste laptop is een betaalbare, robuuste en gebruiksvriendelijke laptop met goede ouderlijk toezicht opties geschikt. Budgetindicatie tot €450. "
            "Specificaties: Een instapmodel processor (Intel Celeron/Pentium, AMD Athlon, of ARM-gebaseerd voor Chromebooks). 4GB RAM. "
            "32GB/64GB eMMC of 128GB opslag. "
            "Een 11 tot 14 inch scherm, HD resolutie is vaak voldoende. "
            "ChromeOS is een uitstekende keuze vanwege eenvoud, veiligheid, ouderlijk toezicht (Family Link) en robuustheid van veel modellen. "
            "Stevige bouwkwaliteit, eventueel morsbestendig toetsenbord. Goede accuduur. "
            "Lichtgewicht en compact."
        )
    },
    "freelancer_general_purpose_non_specialized": {
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Welkom! Ik help u graag met een nieuwe laptop. Wat voor werk doet u voornamelijk?\n"
                "user: Ik ben freelancer en doe allerlei verschillende klussen: teksten schrijven, administratie, wat research, online meetings. Ik zoek een betrouwbare allrounder die niet te traag is.\n"
                "assistant: Een veelzijdige en vlotte laptop dus. Wat is uw budget ongeveer?\n"
                "user: Tussen de 700 en 950 euro. Een goede batterij is wel fijn, want ik werk soms op locatie.\n"
                "assistant: Begrijpelijk. Nog voorkeuren qua schermgrootte of gewicht?\n"
                "user: 14 of 15 inch is prima. Niet te zwaar, gewoon een solide machine."
            ),
            "rankingAlgorithm": "conversation"
        },
        "ground_truth_text": (
            "Voor een freelancer met diverse, niet-gespecialiseerde taken is een betrouwbare allround laptop met goede prestaties, een degelijke accuduur en een comfortabel toetsenbord belangrijk. Budgetindicatie €700-€950. "
            "Specificaties: Een Intel Core i5/i7 (of AMD Ryzen 5/7) van een recente generatie. 16GB RAM wordt aanbevolen voor soepel multitasken. "
            "Een snelle SSD van 512GB. "
            "Een 14 of 15 inch Full HD IPS-scherm. "
            "Accuduur van minimaal 7-8 uur. Gewicht rond 1.5 - 1.8 kg. "
            "Een comfortabel toetsenbord, goede webcam/microfoon en voldoende poorten (USB-A, USB-C, HDMI). "
        )
    },
    "replacing_old_desktop_familiarity": {
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Goedendag! U zoekt een vervanging voor uw oude desktop, begrijp ik?\n"
                "user: Ja, dat klopt. Mijn oude computer is echt aan vervanging toe. Ik zoek een laptop die ik vooral thuis ga gebruiken, voor de gebruikelijke dingen: internet, mail, foto's bekijken, bankzaken. Ik ben Windows gewend.\n"
                "assistant: Een vertrouwde en capabele laptop voor thuisgebruik dus. Wat is uw budget?\n"
                "user: Ik dacht aan zo'n 600 tot 800 euro. Een beetje een vlot ding, en een prettig scherm.\n"
                "assistant: En qua schermgrootte, bent u gewend aan een groot scherm van de desktop?\n"
                "user: Ja, dus een 15 inch of groter zou fijn zijn. Hij hoeft niet per se licht te zijn."
            ),
            "rankingAlgorithm": "conversation"
        },
        "ground_truth_text": (
            "Voor iemand die een oude desktop vervangt en gewend is aan Windows, is een laptop met een comfortabel groot scherm, vlotte prestaties voor alledaagse taken en een vertrouwde interface wenselijk. Budgetindicatie €600-€800. "
            "Specificaties: Een Intel Core i5/i7 (of AMD Ryzen 5/7). 8GB RAM (16GB is een goede upgrade). "
            "Een SSD van minimaal 512GB. "
            "Een 15 inch of 17 inch Full HD IPS-scherm. "
            "Een comfortabel toetsenbord, eventueel met numeriek eiland. Voldoende USB-poorten voor bestaande randapparatuur (muis, printer). HDMI-poort. "
            "Windows. Accuduur is minder kritisch. Focus op een soepele gebruikerservaring."
        )
    },
    "user_focused_on_video_calls_family_abroad": {
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Hallo! Ik help u graag een laptop te vinden. Waarvoor is hij hoofdzakelijk bedoeld?\n"
                "user: Ik wil graag goed kunnen videobellen met mijn familie in het buitenland. Dus een goede camera en microfoon zijn belangrijk. Verder gewoon wat internetten en e-mailen.\n"
                "assistant: Een laptop gericht op communicatie dus. Heeft u een budget in gedachten?\n"
                "user: Rond de 500, maximaal 700 euro. En hij moet makkelijk te bedienen zijn.\n"
                "assistant: Duidelijk. En is er een voorkeur voor schermgrootte of gewicht?\n"
                "user: Een normaal scherm is prima. Gewicht maakt niet zoveel uit, hij blijft toch thuis."
            ),
            "rankingAlgorithm": "conversation"
        },
        "ground_truth_text": (
            "Voor een gebruiker die primair wil videobellen met familie in het buitenland, is een laptop met een uitstekende webcam, goede microfoon, stabiele Wi-Fi en gebruiksgemak essentieel. Budgetindicatie €500-€700. "
            "Specificaties: Een Intel Core i3/i5 (of AMD Ryzen 3/5). 8GB RAM. "
            "Een opslag van minimaal 256GB. "
            "Een 14 of 15 inch Full HD scherm. Focus op modellen die bekend staan om een bovengemiddelde kwaliteit webcam (HD of Full HD) en heldere microfoons. "
            "Stabiele Wi-Fi. Voldoende USB-poorten. "
            "Goede speakers of makkelijke aansluiting voor koptelefoon."
        )
    },
    "diy_craft_hobbyist_patterns_tutorials": {
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Goedendag, u zoekt een laptop. Voor welke hobby's of taken gaat u hem gebruiken?\n"
                "user: Ik doe veel aan handwerken en knutselen. Ik gebruik de laptop om patronen op te zoeken, instructievideo's op YouTube te kijken en soms wat simpele ontwerpen te maken voor mijn snijmachine.\n"
                "assistant: Leuk! Een creatieve hulp dus. Wat is uw budget ongeveer?\n"
                "user: Ongeveer 500 tot 700 euro. Een goed scherm om details te zien is wel fijn.\n"
                "assistant: En is het belangrijk dat hij makkelijk verplaatst kan worden, bijvoorbeeld naar uw hobbytafel?\n"
                "user: Ja, dat zou wel handig zijn, maar hij hoeft niet superlicht te zijn."
            ),
            "rankingAlgorithm": "conversation"
        },
        "ground_truth_text": (
            "Voor een DIY/craft hobbyist die patronen, tutorials bekijkt en lichte ontwerpsoftware gebruikt, is een laptop met een goed, helder scherm en betrouwbare Wi-Fi verbinding belangrijk. Budgetindicatie €500-€700. "
            "Specificaties: Een Intel Core i3/i5 (of AMD Ryzen 3/5). 8GB RAM. "
            "Een SSD van 256GB of 512GB. "
            "Een 14 of 15 inch Full HD IPS-scherm met goede helderheid en redelijke kleurweergave. "
            "Goede Wi-Fi. Voldoende USB-poorten voor aansluiten van eventuele hobby-apparatuur (snijmachine, etc.). "
            "Een touchscreen kan handig zijn voor navigeren door patronen, maar is geen must. "
            "Redelijke accuduur voor flexibel gebruik in huis."
        )
    },
    "budget_conscious_secondary_device_streaming": {
        "api_payload": {
            "category": "Laptop",
            "conversation": (
                "assistant: Hallo, ik help je graag met het vinden van een laptop. Wat wil je er precies mee doen?\n"
                "user: Ik zoek eigenlijk een extra laptopje voor erbij. Vooral om series en films op te streamen in bed of op de bank. Dus een goed scherm en geluid zijn wel belangrijk, maar hij hoeft niet duur te zijn.\n"
                "assistant: Een media-laptop voor een scherpe prijs dus. Wat is je budget maximaal?\n"
                "user: Liefst rond de 400-500 euro. Hij hoeft geen zware taken aan te kunnen.\n"
                "assistant: Duidelijk. Schermgrootte nog een idee, of is vooral de kwaliteit belangrijk?\n"
                "user: Kwaliteit van het scherm is belangrijker, maar niet te klein, zeg 14 inch of zo."
            ),
            "rankingAlgorithm": "conversation"
        },
        "ground_truth_text": (
            "Voor een budgetbewuste gebruiker die een secundaire laptop zoekt primair voor mediaconsumptie (streaming), is een goed scherm en redelijk geluid binnen het budget key. Budgetindicatie €400-€500. "
            "Specificaties: Een Intel Pentium/Celeron, i3 of AMD Athlon/Ryzen 3 (instap). 4GB RAM is minimaal, 8GB is beter voor soepel streamen en browsen. "
            "Een SSD van 128GB of 256GB (of eMMC voor de allerlaagste prijsklasse). "
            "Een 14 of 15 inch Full HD IPS-scherm voor goede kijkhoeken en kleuren. "
            "Redelijke ingebouwde speakers of een goede koptelefoonaansluiting. Stabiele Wi-Fi. "
            "Windows Home of ChromeOS. Accuduur van 6+ uur."
        )
    }
}

ACTIVE_METRICS = [
    answer_relevancy,
    context_precision,
    context_recall,
]

def parse_llm_metric_analysis(llm_output_string):
    parsed_analysis = {}
    lines = llm_output_string.strip().split('\n')
    for line in lines:
        if ':' in line:
            parts = line.split(':', 1)
            metric_name_raw = parts[0].strip()
            explanation = parts[1].strip()
            
            key_name = None
            if metric_name_raw == "Answer Relevancy": key_name = answer_relevancy.name + "_explanation"
            elif metric_name_raw == "Context Precision": key_name = context_precision.name + "_explanation"
            elif metric_name_raw == "Context Recall": key_name = context_recall.name + "_explanation"
            else: 
                cleaned_metric_name = metric_name_raw.lower().replace(" ", "_")
                for metric_obj in ACTIVE_METRICS:
                    if metric_obj.name == cleaned_metric_name:
                        key_name = metric_obj.name + "_explanation"
                        break
                if not key_name:
                    key_name = cleaned_metric_name + "_explanation"
            
            if key_name:
                parsed_analysis[key_name] = explanation
            
    for metric_obj in ACTIVE_METRICS:
        key_to_check = metric_obj.name + "_explanation"
        if key_to_check not in parsed_analysis:
            parsed_analysis[key_to_check] = "LLM heeft geen specifieke verklaring gegeven voor deze metric."
            
    return parsed_analysis

def generate_llm_analysis(ragas_scores, user_input, reference_gt, retrieved_contexts_str_list, recommended_product_names_str):
    if not LLM_AVAILABLE:
        fallback_analysis = {}
        for metric_obj in ACTIVE_METRICS:
            key = metric_obj.name + "_explanation"
            score = ragas_scores.get(metric_obj.name, 1.0) 
            if metric_obj.name == answer_relevancy.name:
                fallback_analysis[key] = f"Answer Relevancy: {'Relevant (score > 0.7).' if score > 0.7 else 'Minder relevant (score <= 0.7), mismatch specs vs vraag.'}"
            elif metric_obj.name == context_precision.name:
                fallback_analysis[key] = f"Context Precision: {'Precies (score > 0.7).' if score > 0.7 else 'Minder precies (score <= 0.7), context bevat mogelijk ruis.'}"
            elif metric_obj.name == context_recall.name:
                fallback_analysis[key] = f"Context Recall: {'Volledig (score > 0.6).' if score > 0.6 else 'Onvolledig (score <= 0.6), context mist mogelijk ideale criteria.'}"
        return {"llm_not_available_fallback": True, **fallback_analysis}

    contexts_for_prompt = "\n\nDetails van Aanbevolen Producten (Retrieved Contexts):\n"
    if not retrieved_contexts_str_list:
        contexts_for_prompt += "Er zijn geen productdetails (retrieved contexts) beschikbaar voor analyse.\n"
    else:
        for i, ctx_str in enumerate(retrieved_contexts_str_list):
            contexts_for_prompt += f"\n--- Product Context {i+1} ---\n{ctx_str}\n--- Einde Product Context {i+1} ---\n"

    ragas_scores_prompt_lines = []
    instructions_prompt_lines = []
    output_format_prompt_lines = []

    if answer_relevancy in ACTIVE_METRICS:
        ragas_scores_prompt_lines.append(f"- Answer Relevancy: {ragas_scores.get(answer_relevancy.name, float('nan')):.2f}")
        instructions_prompt_lines.append("Answer Relevancy: Kernreden waarom de producten wel/niet goed aansluiten bij de gebruikersvraag (noem 1-2 kernspecificaties).")
        output_format_prompt_lines.append("Answer Relevancy: [Jouw verklaring]")
    if context_precision in ACTIVE_METRICS:
        ragas_scores_prompt_lines.append(f"- Context Precision: {ragas_scores.get(context_precision.name, float('nan')):.2f}")
        instructions_prompt_lines.append("Context Precision: Kernreden waarom de productdetails wel/niet to-the-point zijn voor de gebruikersvraag (noem eventueel type ruis).")
        output_format_prompt_lines.append("Context Precision: [Jouw verklaring]")
    if context_recall in ACTIVE_METRICS:
        ragas_scores_prompt_lines.append(f"- Context Recall: {ragas_scores.get(context_recall.name, float('nan')):.2f}")
        instructions_prompt_lines.append("Context Recall: Kernreden waarom de productdetails wel/niet de belangrijkste ideale specificaties dekken (noem 1-2 belangrijkste missende/afwijkende criteria als score < 1.0).")
        output_format_prompt_lines.append("Context Recall: [Jouw verklaring]")

    ragas_scores_str_for_prompt = "\n".join(ragas_scores_prompt_lines)
    instructions_str_for_prompt = "\n".join(instructions_prompt_lines)
    output_format_str_for_prompt = "\n".join(output_format_prompt_lines)

    prompt = f"""
    Je taak is om RAGAS scores voor een laptopaanbeveling KORT en BONDIG te verklaren.
    Vergelijk 'Details van Aanbevolen Producten' met 'Ideale Specificaties' en 'Gebruikersvraag'.
    Geef per RAGAS metric een verklaring van MAXIMAAL ÉÉN ZIN. Focus op de kernreden.
    Als info in 'Details van Aanbevolen Producten' staat, ga ervan uit dat die beschikbaar is.

    Gebruikersvraag:
    "{user_input}"

    Ideale Specificaties (Reference Ground Truth):
    "{reference_gt}"

    {contexts_for_prompt}

    RAGAS Scores (0.0-1.0, hoger is beter):
    {ragas_scores_str_for_prompt}

    Instructies voor output (MAXIMAAL ÉÉN zin per metric, beginnend met de metric naam):
    {instructions_str_for_prompt}

    Output Formaat (exact aanhouden, elke metric op een nieuwe regel):
    {output_format_str_for_prompt}
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Je bent een AI-analist die RAGAS scores uitlegt. Je output is extreem beknopt (maximaal één zin per metric) en volgt het gevraagde formaat."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-4o-mini", 
            temperature=0.0,
            max_tokens=200
        )
        llm_output_string = chat_completion.choices[0].message.content.strip()
        parsed_llm_analysis = parse_llm_metric_analysis(llm_output_string)
        return parsed_llm_analysis
    except Exception as e:
        print(f"Fout tijdens genereren beknopte LLM-analyse: {e}")
        return {"error_generating_analysis": f"Fout bij genereren automatische analyse per metric: {str(e)}"}

def get_recommendations_from_api(api_url, payload):
    response_time_seconds = None # <<< TOEGEVOEGD
    recommendations = None       # <<< TOEGEVOEGD
    try:
        start_time = time.time() # <<< TOEGEVOEGD
        response = requests.post(api_url, json=payload)
        end_time = time.time()   # <<< TOEGEVOEGD
        response_time_seconds = end_time - start_time # <<< TOEGEVOEGD
        response.raise_for_status()
        response_text = response.text
        try:
            recommendations = json.loads(response_text)
        except json.JSONDecodeError:
            clean_response_text = re.sub(r"new ObjectId\('([^']*)'\)", r'"\1"', response_text)
            recommendations = json.loads(clean_response_text)
        return recommendations, response_time_seconds # <<< GEWIJZIGD
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error bij het aanroepen van de API: {http_err}")
        if hasattr(response, 'content'): print(f"Response content: {response.content.decode(errors='ignore')[:500]}...")
        return None, response_time_seconds # <<< GEWIJZIGD (response_time_seconds kan hier een waarde hebben als de error NA de call optreedt)
    except requests.exceptions.RequestException as e:
        print(f"Fout bij het aanroepen van de API: {e}")
        return None, None # <<< GEWIJZIGD (geen call, geen tijd)
    except json.JSONDecodeError as e:
        print(f"Fout bij het parsen van de API JSON response: {e}")
        print(f"Ontvangen tekst (die faalde te parsen): {response_text[:500]}...")
        return None, response_time_seconds # <<< GEWIJZIGD (tijd is er wel, maar parsen faalt)

TOTAL_RUNS = 100
API_URL = "http://localhost:3000/api/products/recommend"
OUTPUT_JSON_ALL_RUNS = "ragas_evaluation_details_multiple_runs.json"
OUTPUT_JSON_OVERALL_STATS = "ragas_overall_statistics.json"
OUTPUT_JSON_PER_PERSONA_STATS = "ragas_per_persona_statistics.json"

all_runs_data_records = []
if os.path.exists(OUTPUT_JSON_ALL_RUNS):
    try:
        with open(OUTPUT_JSON_ALL_RUNS, 'r', encoding='utf-8') as f_in:
            all_runs_data_records = json.load(f_in)
        if not isinstance(all_runs_data_records, list):
            print(f"Warning: Existing data in {OUTPUT_JSON_ALL_RUNS} is not a list. Initializing as empty list.")
            all_runs_data_records = []
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from {OUTPUT_JSON_ALL_RUNS}. Initializing as empty list.")
        all_runs_data_records = []

persona_ids_to_run = list(persona_data_store.keys())
num_personas = len(persona_ids_to_run)
if num_personas == 0:
    print("FOUT: Geen personas gedefinieerd in persona_data_store. Script stopt.")
    exit()

print(f"--- STARTING {TOTAL_RUNS} EVALUATION RUNS ACROSS {num_personas} PERSONAS ---")

for i in tqdm(range(TOTAL_RUNS), desc="Overall Progress"):
    selected_persona_id = persona_ids_to_run[i % num_personas]
    run_number = i + 1
    print(f"\n--- RUN {run_number}/{TOTAL_RUNS} - PERSONA: '{selected_persona_id}' ---")

    current_persona_config = persona_data_store[selected_persona_id]
    current_api_payload = current_persona_config["api_payload"]
    ground_truth_ragas = current_persona_config["ground_truth_text"]

    gesprek_input_voor_ragas = ""
    conversation_data = current_api_payload.get('conversation')
    if isinstance(conversation_data, str):
        user_parts = []
        for line in conversation_data.strip().split('\n'):
            if line.lower().startswith("user:"):
                user_parts.append(line[len("user:"):].strip())
        if user_parts:
            gesprek_input_voor_ragas = " ".join(user_parts)
        else:
            gesprek_input_voor_ragas = conversation_data
    else:
        gesprek_input_voor_ragas = "Gebruikersinput niet beschikbaar."
        print(f"Warning: Onverwacht type of ontbrekende 'conversation' data voor persona {selected_persona_id}.")

    api_response_data, api_responsetime_seconds = get_recommendations_from_api(API_URL, current_api_payload) # <<< GEWIJZIGD

    aanbevelingen_lijst = None
    if api_response_data:
        if isinstance(api_response_data, list):
            aanbevelingen_lijst = api_response_data
        elif isinstance(api_response_data, dict) and 'recommendations' in api_response_data and isinstance(api_response_data['recommendations'], list):
            aanbevelingen_lijst = api_response_data['recommendations']
        elif isinstance(api_response_data, dict):
            potential_list = [v for v in api_response_data.values() if isinstance(v, list)]
            if potential_list and all(isinstance(item, dict) and 'product' in item for item in potential_list[0]):
                 aanbevelingen_lijst = potential_list[0]

    if not aanbevelingen_lijst or not isinstance(aanbevelingen_lijst, list) or not aanbevelingen_lijst:
        print(f"Geen valide aanbevelingen ontvangen of geëxtraheerd voor persona '{selected_persona_id}' in run {run_number}. RAGAS evaluatie wordt overgeslagen.")
        current_timestamp = datetime.datetime.now().isoformat()
        error_record = {
            "timestamp": current_timestamp,
            "run_number": run_number,
            "persona_id": selected_persona_id,
            "status": "API_FAILURE_OR_NO_RECOMMENDATIONS",
            "user_input": gesprek_input_voor_ragas,
            "api_response_sample": str(api_response_data)[:200] if api_response_data else "None",
            "api_responsetime_seconds": api_responsetime_seconds # <<< TOEGEVOEGD
        }
        all_runs_data_records.append(error_record)
        with open(OUTPUT_JSON_ALL_RUNS, 'w', encoding='utf-8') as f_details:
            json.dump(all_runs_data_records, f_details, indent=4, ensure_ascii=False, allow_nan=True)
        continue

    try:
        answer_ragas_list = []
        for p_item_wrapper in aanbevelingen_lijst:
            p_item = None
            if isinstance(p_item_wrapper, dict) and 'product' in p_item_wrapper and isinstance(p_item_wrapper['product'], dict):
                p_item = p_item_wrapper['product']
            elif isinstance(p_item_wrapper, dict) and 'name' in p_item_wrapper:
                 p_item = p_item_wrapper
            if p_item and 'name' in p_item:
                answer_ragas_list.append(p_item['name'])
        
        if answer_ragas_list:
            product_names_only = ", ".join(answer_ragas_list)
            answer_ragas = f"Gebaseerd op uw vraag, zijn de volgende producten aanbevolen: {product_names_only}."
        else:
            answer_ragas = "Kon geen productnamen extraheren uit de aanbevelingen."
            print(f"Warning: Kon geen productnamen extraheren voor RAGAS answer (Persona: {selected_persona_id}, Run: {run_number}).")

        contexts_ragas = []
        for rec_item_wrapper in aanbevelingen_lijst:
            prod = None
            if isinstance(rec_item_wrapper, dict) and 'product' in rec_item_wrapper and isinstance(rec_item_wrapper['product'], dict):
                prod = rec_item_wrapper['product']
            elif isinstance(rec_item_wrapper, dict) and 'name' in rec_item_wrapper:
                prod = rec_item_wrapper
            if not prod: continue

            feature_strings = []
            for feat in prod.get('features', []): 
                if isinstance(feat, dict):
                    f_name = feat.get('featureName', 'N/A')
                    f_tier = feat.get('tier', 'N/A')
                    f_expl = feat.get('explanation', 'N/A')
                    feature_strings.append(f"{f_name}: {f_tier} ({f_expl})")
            contexts_ragas.append(f"Product: {prod.get('name', 'N/A')}. Prijs: {prod.get('price', 'N/A')}. Categorie: {prod.get('category', 'N/A')}. Features: {'; '.join(feature_strings) if feature_strings else 'Geen features beschikbaar'}")

        if not contexts_ragas or answer_ragas == "Kon geen productnamen extraheren uit de aanbevelingen.":
            print(f"Geen valide contexten en/of antwoord gegenereerd voor persona '{selected_persona_id}' in run {run_number}. RAGAS evaluatie wordt overgeslagen.")
            current_timestamp = datetime.datetime.now().isoformat()
            error_record_ragas_prep = {
                "timestamp": current_timestamp,
                "run_number": run_number,
                "persona_id": selected_persona_id,
                "status": "RAGAS_PREP_FAILURE",
                "user_input": gesprek_input_voor_ragas,
                "answer_ragas": answer_ragas,
                "contexts_ragas_count": len(contexts_ragas),
                "api_responsetime_seconds": api_responsetime_seconds # <<< TOEGEVOEGD
            }
            all_runs_data_records.append(error_record_ragas_prep)
            with open(OUTPUT_JSON_ALL_RUNS, 'w', encoding='utf-8') as f_details:
                json.dump(all_runs_data_records, f_details, indent=4, ensure_ascii=False, allow_nan=True)
            continue

        dataset_dict = {
            "question": [gesprek_input_voor_ragas],
            "answer": [answer_ragas],
            "contexts": [contexts_ragas],
            "ground_truth": [ground_truth_ragas]
        }
        dataset = Dataset.from_dict(dataset_dict)
        result = evaluate(dataset, metrics=ACTIVE_METRICS) 
        df_results_current_run = result.to_pandas()

        ragas_scores_dict = {}
        if hasattr(result, 'scores') and isinstance(result.scores, dict):
            ragas_scores_dict = result.scores
        elif isinstance(result, dict):
             ragas_scores_dict = {k: (v if v is not None else float('nan')) for k,v in result.items() if k in [m.name for m in ACTIVE_METRICS]}

        if not df_results_current_run.empty:
            score_column_names = [metric.name for metric in ACTIVE_METRICS]
            try: 
                existing_score_cols = [col for col in score_column_names if col in df_results_current_run.columns]
                if existing_score_cols:
                    scores_series = df_results_current_run.iloc[0][existing_score_cols]
                    for col_name, score_val in scores_series.to_dict().items():
                        if col_name not in ragas_scores_dict or pd.isna(ragas_scores_dict.get(col_name)):
                            ragas_scores_dict[col_name] = score_val if not pd.isna(score_val) else float('nan')
            except (KeyError, IndexError) as e: 
                print(f"Waarschuwing: Fout bij RAGAS scores uit DataFrame halen voor run {run_number}. Fout: {e}")
        
        for metric_obj in ACTIVE_METRICS:
            if metric_obj.name not in ragas_scores_dict:
                ragas_scores_dict[metric_obj.name] = float('nan')
        
        parsed_llm_analysis_dict = generate_llm_analysis(
            ragas_scores_dict,
            gesprek_input_voor_ragas,
            ground_truth_ragas,
            contexts_ragas,
            answer_ragas
        )

        current_timestamp = datetime.datetime.now().isoformat()
        current_run_record_data = {}
        if not df_results_current_run.empty:
            current_run_record_data = df_results_current_run.iloc[0].to_dict()

        final_record_for_json = {
            "timestamp": current_timestamp,
            "run_number": run_number,
            "persona_id": selected_persona_id,
            "user_input": current_run_record_data.get("question", gesprek_input_voor_ragas),
            "response_generated_for_ragas": current_run_record_data.get("answer", answer_ragas),
            "reference_ground_truth": current_run_record_data.get("ground_truth", ground_truth_ragas),
            "api_responsetime_seconds": api_responsetime_seconds, # <<< TOEGEVOEGD
            "llm_metric_explanations": parsed_llm_analysis_dict,
            "retrieved_contexts_for_ragas": current_run_record_data.get("contexts", contexts_ragas)
        }
        for metric_obj in ACTIVE_METRICS:
            final_record_for_json[metric_obj.name] = ragas_scores_dict.get(metric_obj.name)
        
        all_runs_data_records.append(final_record_for_json)
        with open(OUTPUT_JSON_ALL_RUNS, 'w', encoding='utf-8') as f_details:
            json.dump(all_runs_data_records, f_details, indent=4, ensure_ascii=False, allow_nan=True)
        
    except TypeError as te:
        print(f"TypeError TIJDENS verwerken van RAGAS data voor persona '{selected_persona_id}' in run {run_number}: {te}")
        import traceback; traceback.print_exc()
    except Exception as e:
        print(f"Algemene fout TIJDENS RAGAS evaluatie voor persona '{selected_persona_id}' in run {run_number}: {e}")
        import traceback; traceback.print_exc()

print(f"\n--- COMPLETED {TOTAL_RUNS} EVALUATION RUNS ---")
print(f"All detailed results saved to {OUTPUT_JSON_ALL_RUNS}")

if all_runs_data_records:
    active_metric_proxy_name = ACTIVE_METRICS[0].name if ACTIVE_METRICS else None
    scored_records = []
    if active_metric_proxy_name: # We check for at least one RAGAS metric AND responsetime
        scored_records = [
            r for r in all_runs_data_records
            if isinstance(r, dict) and 
               active_metric_proxy_name in r and r.get(active_metric_proxy_name) is not None and
               "api_responsetime_seconds" in r and r.get("api_responsetime_seconds") is not None
        ]
    else: # Fallback if no RAGAS metrics, but still want responsetime if available
         scored_records = [
            r for r in all_runs_data_records
            if isinstance(r, dict) and "api_responsetime_seconds" in r and r.get("api_responsetime_seconds") is not None
        ]

    if not scored_records:
        print("No successfully scored records with API response time found to calculate statistics.")
    # Removed ELIF not ACTIVE_METRICS, as we might still have responsetime
    else:
        df_all_runs = pd.DataFrame(scored_records)
        
        # Metric names for RAGAS scores + API response time
        metric_names_for_stats = [m.name for m in ACTIVE_METRICS]
        performance_metric_name = "api_responsetime_seconds" # <<< TOEGEVOEGD
        all_cols_for_stats = metric_names_for_stats + [performance_metric_name] # <<< TOEGEVOEGD
        
        for col in all_cols_for_stats: # <<< GEWIJZIGD
            if col in df_all_runs.columns:
                df_all_runs[col] = pd.to_numeric(df_all_runs[col], errors='coerce')
            else: 
                df_all_runs[col] = pd.Series(dtype='float')

        print("\n" + "="*30 + " SUMMARY STATISTICS " + "="*30)

        print("\n--- OVERALL STATISTICS (ACROSS ALL SUCCESSFUL RUNS) ---")
        overall_stats_df = df_all_runs[all_cols_for_stats].agg(['mean', 'min', 'max', 'std', 'count']) # <<< GEWIJZIGD
        print(overall_stats_df)
        
        overall_stats_df_transposed = overall_stats_df.T 
        overall_stats_json_readable = overall_stats_df_transposed.to_dict(orient="index") 
        
        with open(OUTPUT_JSON_OVERALL_STATS, "w", encoding="utf-8") as f_json:
            json.dump(overall_stats_json_readable, f_json, indent=4)
        print(f"\nOverall statistics saved to {OUTPUT_JSON_OVERALL_STATS}")

        print("\n--- DETAILS FOR OVERALL MIN/MAX SCORING RUNS (CONSOLE) ---")
        for metric_name in all_cols_for_stats: # <<< GEWIJZIGD
            if not df_all_runs[metric_name].dropna().empty:
                idx_max = df_all_runs[metric_name].idxmax()
                max_score_run_details = df_all_runs.loc[idx_max]
                
                # Adjust wording for response time
                if metric_name == performance_metric_name:
                    print(f"\n  Metric: {metric_name} - SLOWEST (Max) Time: {max_score_run_details[metric_name]:.4f} seconds")
                else:
                    print(f"\n  Metric: {metric_name} - PEAK (Max) Score: {max_score_run_details[metric_name]:.4f}")
                
                print(f"    Run Number: {max_score_run_details.get('run_number', 'N/A')}")
                print(f"    Persona ID: {max_score_run_details.get('persona_id', 'N/A')}")
                print(f"    User Input (snippet): {str(max_score_run_details.get('user_input', 'N/A'))[:150]}...")
                
                if metric_name != performance_metric_name and 'llm_metric_explanations' in max_score_run_details and \
                   isinstance(max_score_run_details['llm_metric_explanations'], dict):
                    explanation_key = metric_name + "_explanation"
                    specific_explanation = max_score_run_details['llm_metric_explanations'].get(explanation_key, "Explanation not available for this metric.")
                    print(f"    LLM Explanation for this run's {metric_name}: {specific_explanation}")
                elif metric_name != performance_metric_name:
                     print(f"    LLM Explanations field not found or malformed for this run.")

                idx_min = df_all_runs[metric_name].idxmin()
                min_score_run_details = df_all_runs.loc[idx_min]

                if metric_name == performance_metric_name:
                     print(f"\n  Metric: {metric_name} - FASTEST (Min) Time: {min_score_run_details[metric_name]:.4f} seconds")
                else:
                    print(f"\n  Metric: {metric_name} - LOW (Min) Score: {min_score_run_details[metric_name]:.4f}")

                print(f"    Run Number: {min_score_run_details.get('run_number', 'N/A')}")
                print(f"    Persona ID: {min_score_run_details.get('persona_id', 'N/A')}")
                print(f"    User Input (snippet): {str(min_score_run_details.get('user_input', 'N/A'))[:150]}...")

                if metric_name != performance_metric_name and 'llm_metric_explanations' in min_score_run_details and \
                   isinstance(min_score_run_details['llm_metric_explanations'], dict):
                    explanation_key = metric_name + "_explanation"
                    specific_explanation = min_score_run_details['llm_metric_explanations'].get(explanation_key, "Explanation not available for this metric.")
                    print(f"    LLM Explanation for this run's {metric_name}: {specific_explanation}")
                elif metric_name != performance_metric_name:
                    print(f"    LLM Explanations field not found or malformed for this run.")
            else:
                print(f"\n  Metric: {metric_name} - No valid scores/times to determine min/max.")

        print("\n\n--- STATISTICS PER PERSONA ---")
        per_persona_stats_for_json = {} 
        for persona_id, group_df in df_all_runs.groupby("persona_id"):
            print(f"\n  Persona: {persona_id}")
            persona_stats_df = group_df[all_cols_for_stats].agg(['mean', 'min', 'max', 'std', 'count']) # <<< GEWIJZIGD
            print(persona_stats_df)
            
            persona_stats_df_transposed = persona_stats_df.T
            per_persona_stats_for_json[persona_id] = persona_stats_df_transposed.to_dict(orient="index")

            for metric_name in all_cols_for_stats: # <<< GEWIJZIGD
                if not group_df[metric_name].dropna().empty:
                    idx_max_persona = group_df[metric_name].idxmax()
                    max_persona_run_details = df_all_runs.loc[idx_max_persona] # Use df_all_runs to get full record
                    if metric_name == performance_metric_name:
                        print(f"    Metric: {metric_name} - SLOWEST (Max) for {persona_id}: {max_persona_run_details[metric_name]:.4f}s (Run: {max_persona_run_details.get('run_number', 'N/A')})")
                    else:
                        print(f"    Metric: {metric_name} - PEAK (Max) for {persona_id}: {max_persona_run_details[metric_name]:.4f} (Run: {max_persona_run_details.get('run_number', 'N/A')})")

                    idx_min_persona = group_df[metric_name].idxmin()
                    min_persona_run_details = df_all_runs.loc[idx_min_persona] # Use df_all_runs to get full record
                    if metric_name == performance_metric_name:
                        print(f"    Metric: {metric_name} - FASTEST (Min) for {persona_id}: {min_persona_run_details[metric_name]:.4f}s (Run: {min_persona_run_details.get('run_number', 'N/A')})")
                    else:
                        print(f"    Metric: {metric_name} - LOW (Min) for {persona_id}: {min_persona_run_details[metric_name]:.4f} (Run: {min_persona_run_details.get('run_number', 'N/A')})")
                else:
                    print(f"    Metric: {metric_name} - No valid scores/times for this persona.")


        if per_persona_stats_for_json:
            with open(OUTPUT_JSON_PER_PERSONA_STATS, "w", encoding="utf-8") as f_json:
                json.dump(per_persona_stats_for_json, f_json, indent=4)
            print(f"\nPer-persona statistics saved to {OUTPUT_JSON_PER_PERSONA_STATS}")

        print("\n" + "="*25 + " END OF SUMMARY STATISTICS " + "="*25)
else:
    print("No data records were collected. Cannot calculate statistics.")