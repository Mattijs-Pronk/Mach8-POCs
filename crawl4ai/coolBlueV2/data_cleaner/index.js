const fs = require('fs'); // Import the fs module

const rawData = [
    {
        "name": "Acer Chromebook 317 CB317-1H-C1SE",
        "rating": "9,3/10 (15 reviews)",
        "price": "399,-",
        "product_specifications": "ProductArtikelnummer886844FabrikantcodeNX.AQ2EH.004MerkAcerGarantie2 jaarAfhandeling van je defectVia CoolblueOude apparaat gratis retourJaBelangrijkste eigenschappenBesturingssysteemGoogle Chrome OSSchermdiagonaal17,3 inchProcessorIntel CeleronIntern werkgeheugen (RAM)4 GBTotale opslagcapaciteit64 GBVideokaart chipsetIntel UHD GraphicsTouchscreenNeeType usb-aansluitingStandaard usb-A, Usb-CAanbevolen voor gebruik laptopsFilms en series streamen, Internet, email en tekstverwerkenSnelheidsklasse laptopsBasisklasseBouwkwaliteit laptopsBasisklasseBeeldschermSchermdiagonaal17,3 inchScherpteFull HD (1080p)Resolutie breedte1920 pixelsResolutie hoogte1080 pixelsVerversingssnelheid60 HzTouchscreenNeeReflectie schermAnti reflecterendPaneeltypeIPS paneelAdaptive SyncNeeProcessorProcessorIntel CeleronProcessor cijferN4500Processor kernenDual core (2)Processor codenaamJasper LakeKloksnelheid1,1 GHzTurbo snelheid2,8 GHzCachegeheugen4 MBIntel Evo laptopNeeWerkgeheugenIntern werkgeheugen (RAM)4 GBSamenstelling geheugen1 x 4 GBGeheugenslot 14 GBTotaal aantal RAM geheugensloten1OpslagType opslagFlashTotale opslagcapaciteit64 GBOpslagcapaciteit van SSD64 GBType harde schijfeMMCVideokaartVideokaart chipsetIntel UHD GraphicsSoort videokaartSharedBesturingssysteemBesturingssysteemGoogle Chrome OSTaal besturingssysteemMeerdere talen in te stellenFysieke eigenschappenModel laptopLaptopKleurZilverMateriaalKunststofHoogte2,25 cmBreedte40,12 cmDiepte26,7 cmGewicht2,2 kgBouwkwaliteit laptopsBasisklasseDraadloze verbindingenMobiele dataconnectieGeenBluetoothJaBluetooth-versie5.0Bedrade verbindingenUsb-aansluitingJaAantal usb-aansluitingen4Type usb-aansluitingStandaard usb-A, Usb-CProtocol Female usb-C poortDisplayPort Alternatieve Modus, Thunderbolt Alternatieve Modus, USB, USB elektriciteitUsb versie Female usb-C poort3.1Video output via usb C mogelijkJaAantal female standaard usb-A poorten2Versie female standaard usb-A poort3.1Aantal usb 3.1 Female usb-C poort2HDMI-aansluitingNeeDisplayPort-aansluitingNeeVGA-aansluitingNeeThunderbolt-aansluitingNeeHoofdtelefoon aansluitingJaGeheugenkaartlezerJaToetsenbord en touchpadToetsenbordindelingQWERTYFysieke toetsenbordindelingANSINumeriek toetsenblokJaMorsbestendigNeeVerlicht toetsenbordNeeMechanische toetsenNeeProgrammeerbare toetsenNeeAudioIngebouwde microfoonJaAantal speakers2GeluidsweergaveStereoMerk van ingebouwde computer luidsprekersStandaard luidsprekersWebcamIngebouwde cameraJaBeeld-definitie webcamsHD Ready (720p)AccuAccu/batterij technologieLithium-ionMaximale accu/batterijduur4,5 uurExtra fabrieksgarantieFabrieksgarantieNeeBeveiligingTPM (Trusted platform module)JaKensington slotNeeWindows HelloNeeVingerafdruk-identiteitssensorNeeVeiligheidsklasse laptopsMiddenklasseUitbreidingsmogelijkhedenAantal vrije RAM geheugensloten0SoftwareExtra ge\u00efnstalleerde softwareNee",
        "url": "https://www.coolblue.nl/product/886844/acer-chromebook-317-cb317-1h-c1se.html"
    },
    {
        "name": "Acer Chromebook 317 CB317-1H-C6RN",
        "rating": "9,3/10 (15 reviews)",
        "price": "469,-",
        "product_specifications": "ProductArtikelnummer886845FabrikantcodeNX.AQ1EH.003MerkAcerGarantie2 jaarAfhandeling van je defectVia CoolblueOude apparaat gratis retourJaBelangrijkste eigenschappenBesturingssysteemGoogle Chrome OSSchermdiagonaal17,3 inchProcessorIntel CeleronIntern werkgeheugen (RAM)8 GBTotale opslagcapaciteit128 GBVideokaart chipsetIntel UHD GraphicsTouchscreenNeeType usb-aansluitingStandaard usb-A, Usb-CAanbevolen voor gebruik laptopsFilms en series streamen, Internet, email en tekstverwerkenSnelheidsklasse laptopsBasisklasseBouwkwaliteit laptopsBasisklasseBeeldschermSchermdiagonaal17,3 inchScherpteFull HD (1080p)Resolutie breedte1920 pixelsResolutie hoogte1080 pixelsVerversingssnelheid60 HzTouchscreenNeeReflectie schermAnti reflecterendPaneeltypeIPS paneelAdaptive SyncNeeProcessorProcessorIntel CeleronProcessor cijferN5100Processor kernenQuad core (4)Processor codenaamJasper LakeKloksnelheid1,1 GHzTurbo snelheid2,8 GHzCachegeheugen4 MBIntel Evo laptopNeeWerkgeheugenIntern werkgeheugen (RAM)8 GBSamenstelling geheugen1 x 8 GBGeheugenslot 18 GBTotaal aantal RAM geheugensloten1OpslagType opslagFlashTotale opslagcapaciteit128 GBOpslagcapaciteit van SSD128 GBType harde schijfeMMCVideokaartVideokaart chipsetIntel UHD GraphicsSoort videokaartSharedBesturingssysteemBesturingssysteemGoogle Chrome OSTaal besturingssysteemMeerdere talen in te stellenFysieke eigenschappenModel laptopLaptopKleurZilverMateriaalKunststofHoogte2,25 cmBreedte40,12 cmDiepte26,7 cmGewicht2,2 kgBouwkwaliteit laptopsBasisklasseDraadloze verbindingenMobiele dataconnectieGeenBluetoothJaBluetooth-versie5.0Bedrade verbindingenUsb-aansluitingJaAantal usb-aansluitingen4Type usb-aansluitingStandaard usb-A, Usb-CProtocol Female usb-C poortDisplayPort Alternatieve Modus, Thunderbolt Alternatieve Modus, USB, USB elektriciteitUsb versie Female usb-C poort3.1Video output via usb C mogelijkJaAantal female standaard usb-A poorten2Versie female standaard usb-A poort3.1Aantal usb 3.1 Female usb-C poort2HDMI-aansluitingNeeDisplayPort-aansluitingNeeVGA-aansluitingNeeThunderbolt-aansluitingNeeHoofdtelefoon aansluitingJaGeheugenkaartlezerJaToetsenbord en touchpadToetsenbordindelingQWERTYFysieke toetsenbordindelingANSINumeriek toetsenblokJaMorsbestendigNeeVerlicht toetsenbordNeeMechanische toetsenNeeProgrammeerbare toetsenNeeAudioIngebouwde microfoonJaAantal speakers2GeluidsweergaveStereoMerk van ingebouwde computer luidsprekersStandaard luidsprekersWebcamIngebouwde cameraJaBeeld-definitie webcamsHD Ready (720p)AccuAccu/batterij technologieLithium-ionMaximale accu/batterijduur4,5 uurExtra fabrieksgarantieFabrieksgarantieNeeBeveiligingTPM (Trusted platform module)JaKensington slotNeeWindows HelloNeeVingerafdruk-identiteitssensorNeeVeiligheidsklasse laptopsMiddenklasseUitbreidingsmogelijkhedenAantal vrije RAM geheugensloten0SoftwareExtra ge\u00efnstalleerde softwareNee",
        "url": "https://www.coolblue.nl/product/886845/acer-chromebook-317-cb317-1h-c6rn.html"
    }
];

// Functie om een JSON-schema te genereren uit de eerste specificaties
const generateSchema = (specStr) => {
    const specObj = {};
    const lines = specStr.match(/([A-Za-z\s]+)([\d\w\s%]+)/g);

    if (lines) {
        lines.forEach(line => {
            const match = line.match(/^([\w\s]+?)(\d[\d\w\s%]*)$/); // Key-Value splitsing
            if (match) {
                let key = match[1].trim().replace(/\s+/g, '_').toLowerCase(); // Maak key geschikt voor JSON
                let value = match[2].trim();
                specObj[key] = value;
            }
        });
    }
    return specObj;
};

// Genereer schema op basis van eerste product
const exampleProduct = rawData[0];
const schema = generateSchema(exampleProduct.product_specifications);

// Functie om het schema toe te passen op een product
const applySchema = (specStr, schema) => {
    const specObj = {};
    for (const key in schema) {
        const regex = new RegExp(key.replace(/_/g, '\\s*') + '\\s*([\\d\\w\\s%]+)');
        const match = specStr.match(regex);
        specObj[key] = match ? match[1].trim() : null;
    }
    return specObj;
};

// Verwerk alle producten volgens het schema
const cleanedData = rawData.map(product => ({
    name: product.name,
    ...parseRating(product.rating),
    price: parsePrice(product.price),
    specifications: applySchema(product.product_specifications, schema),
    url: product.url
}));

// Opslaan naar bestand
fs.writeFileSync('cleanedData.json', JSON.stringify(cleanedData, null, 2), 'utf-8');

console.log("Data opgeschoond en opgeslagen in cleanedData.json");

