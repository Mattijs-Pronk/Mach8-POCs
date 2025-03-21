houseSchemaDTO = {
  "name": "Houses",
  "baseSelector": "div.relative.m-auto.mt-6.flex.max-w-screen-lg.flex-col.gap-0.px-4.lg\\:grid.lg\\:grid-cols-\\[7fr_3fr\\].lg\\:gap-6",
  "fields": [
    {
      "name": "address",
      "selector": "span.text-2xl.font-bold",
      "type": "text"
    },
    {
      "name": "postal code and location",
      "selector": "span.text-neutral-40",
      "type": "text"
    },
    {
      "name": "real estate project",
      "selector": "a[aria-label]",
      "type": "text"
    },
    {
      "name": "Asking Price",
      "selector": "div h3:contains('Overdracht') + dl dt:nth-of-type(1) + dd span.mr-2",
      "type": "text"
    },
    
    {
      "name": "Asking Price per m²",
      "selector": "div h3:contains('Overdracht') + dl dt:nth-of-type(2) + dd span.mr-2",
      "type": "text"
    },
    {
      "name": "Available Since",
      "selector": "div h3:contains('Overdracht') + dl dt:nth-of-type(3) + dd button",
      "type": "text"
    },
    {
      "name": "Status",
      "selector": "div h3:contains('Overdracht') + dl dt:nth-of-type(4) + dd",
      "type": "text"
    },
    {
      "name": "Acceptance",
      "selector": "div h3:contains('Overdracht') + dl dt:nth-of-type(5) + dd",
      "type": "text"
    },
    {
      "name": "Type of House",
      "selector": "div h3:contains('Bouw') + dl dt:nth-of-type(1) + dd",
      "type": "text"
    },
    {
      "name": "Type of Construction",
      "selector": "div h3:contains('Bouw') + dl dt:nth-of-type(2) + dd",
      "type": "text"
    },
    {
      "name": "Year of Construction",
      "selector": "div h3:contains('Bouw') + dl dt:nth-of-type(3) + dd",
      "type": "text"
    },
    {
      "name": "Specific",
      "selector": "div h3:contains('Bouw') + dl dt:nth-of-type(4) + dd",
      "type": "text"
    },
    {
      "name": "Roof Type",
      "selector": "div h3:contains('Bouw') + dl dt:nth-of-type(5) + dd",
      "type": "text"
    },
    {
      "name": "Living Area",
      "selector": "div h3:contains('Oppervlakten en inhoud') + dl dt:nth-of-type(2) + dd",
      "type": "text"
    },
    {
      "name": "Other Indoor Space",
      "selector": "div h3:contains('Oppervlakten en inhoud') + dl dt:nth-of-type(3) + dd",
      "type": "text"
    },
    {
      "name": "External Storage Space",
      "selector": "div h3:contains('Oppervlakten en inhoud') + dl dt:nth-of-type(4) + dd",
      "type": "text"
    },
    {
      "name": "Plot",
      "selector": "div h3:contains('Oppervlakten en inhoud') + dl dt:nth-of-type(5) + dd",
      "type": "text"
    },
    {
      "name": "Volume",
      "selector": "div h3:contains('Oppervlakten en inhoud') + dl dt:nth-of-type(6) + dd",
      "type": "text"
    },
    {
      "name": "Number of Rooms",
      "selector": "div h3:contains('Indeling') + dl dt:nth-of-type(1) + dd",
      "type": "text"
    },
    {
      "name": "Number of Bathrooms",
      "selector": "div h3:contains('Indeling') + dl dt:nth-of-type(2) + dd",
      "type": "text"
    },
    {
      "name": "Bathroom Facilities",
      "selector": "div h3:contains('Indeling') + dl dt:nth-of-type(3) + dd",
      "type": "text"
    },
    {
      "name": "Number of Floors",
      "selector": "div h3:contains('Indeling') + dl dt:nth-of-type(4) + dd",
      "type": "text"
    },
    {
      "name": "Facilities",
      "selector": "div h3:contains('Indeling') + dl dt:nth-of-type(5) + dd",
      "type": "text"
    },
    {
      "name": "Energy Label",
      "selector": "div h3:contains('Energie') + dl dt:nth-of-type(1) + dd span.bg-[#009342]",
      "type": "text"
    },
    {
      "name": "Energy Label Meaning",
      "selector": "div h3:contains('Energie') + dl dt:nth-of-type(1) + dd a",
      "type": "text"
    },
    {
      "name": "Insulation",
      "selector": "div h3:contains('Energie') + dl dt:nth-of-type(2) + dd",
      "type": "text"
    },
    {
      "name": "Heating",
      "selector": "div h3:contains('Energie') + dl dt:nth-of-type(3) + dd",
      "type": "text"
    },
    {
      "name": "Hot Water",
      "selector": "div h3:contains('Energie') + dl dt:nth-of-type(4) + dd",
      "type": "text"
    },
    {
      "name": "Boiler",
      "selector": "div h3:contains('Energie') + dl dt:nth-of-type(5) + dd",
      "type": "text"
    },
    {
      "name": "Cadastral Information",
      "selector": "h3:contains('Kadastrale gegevens') + dl dt:nth-of-type(1)",
      "type": "text"
    },
    {
      "name": "Cadastral Map",
      "selector": "h3:contains('Kadastrale gegevens') + dl dd a",
      "type": "text"
    },
    {
      "name": "Surface Area (Cadastral)",
      "selector": "h3:contains('Kadastrale gegevens') + dl dt:nth-of-type(2) + dd",
      "type": "text"
    },
    {
      "name": "Ownership Situation",
      "selector": "h3:contains('Kadastrale gegevens') + dl dt:nth-of-type(3) + dd",
      "type": "text"
    },
    {
      "name": "Outdoor Area Location",
      "selector": "h3:contains('Buitenruimte') + dl dt:nth-of-type(1) + dd",
      "type": "text"
    },
    {
      "name": "Garden",
      "selector": "h3:contains('Buitenruimte') + dl dt:nth-of-type(2) + dd",
      "type": "text"
    },
    {
      "name": "Back Garden",
      "selector": "h3:contains('Buitenruimte') + dl dt:nth-of-type(3) + dd",
      "type": "text"
    },
    {
      "name": "Garden Location",
      "selector": "h3:contains('Buitenruimte') + dl dt:nth-of-type(4) + dd",
      "type": "text"
    },
    {
      "name": "Shed/Storage",
      "selector": "h3:contains('Bergruimte') + dl dt:nth-of-type(1) + dd",
      "type": "text"
    },
    {
      "name": "Storage Facilities",
      "selector": "h3:contains('Bergruimte') + dl dt:nth-of-type(2) + dd",
      "type": "text"
    },
    {
      "name": "Storage Insulation",
      "selector": "h3:contains('Bergruimte') + dl dt:nth-of-type(3) + dd",
      "type": "text"
    },
    {
      "name": "Garage Type",
      "selector": "h3:contains('Garage') + dl dt:nth-of-type(1) + dd",
      "type": "text"
    },
    {
      "name": "Garage Capacity",
      "selector": "h3:contains('Garage') + dl dt:nth-of-type(2) + dd",
      "type": "text"
    },
    {
      "name": "Garage Facilities",
      "selector": "h3:contains('Garage') + dl dt:nth-of-type(3) + dd",
      "type": "text"
    },
    {
      "name": "Garage Insulation",
      "selector": "h3:contains('Garage') + dl dt:nth-of-type(4) + dd",
      "type": "text"
    },
    {
      "name": "Parking Type",
      "selector": "h3:contains('Parkeergelegenheid') + dl dt:nth-of-type(1) + dd",
      "type": "text"
    },
    {
      "name": "Description",
      "selector": "#headlessui-disclosure-panel-v-0-0-1",
      "type": "text"
    }
  ]
}
