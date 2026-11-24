# Golok AI Trading Lab Pro ચલાવવાની રીત

1. તમારા સ્થાનિક Odoo 20નું સામાન્ય launcher ચાલુ કરો અને તેનો localhost સરનામો ખોલો. Appsમાં **Golok AI Trading Lab Pro** ઇન્સ્ટોલ અથવા અપગ્રેડ કરો. સક્રિય કંપની પસંદ કરો અને **Trading Lab → Research Overview** ખોલો.
2. બ્રોકર વગર અજમાવવા પોતાના બનાવેલા candles માટે **Synthetic fixture** પસંદ કરો. છેલ્લી candleનો સમય, importનો સમય અને data origin અલગથી વાંચો. દૈનિક Bhavcopy સત્ર પૂરું થયા પછીનો ડેટા છે.
3. **Source Authorizations**માં administrator સ્રોત, ઉપયોગ, શરતો, પુરાવો અને મંજૂરીની અંતિમ તારીખ નોંધે. ક્વેરી, ડિસ્પ્લે અને કાયમી આંતરિક સંગ્રહની મંજૂરી હોય ત્યારે જ તે અધિકારો પસંદ કરો. **End-of-day File Imports**માં સ્રોત, પૂરી થયેલી તારીખ અને NSE કૅલેન્ડર પસંદ કરીને ફાઇલ આપો. **Quarantined** દેખાય તો તારીખ, format અને ભાવ ચકાસો.
4. **Run Synthetic Portfolio**માં અલગ instrumentsના datasets, તારીખો અને hypothetical tariff પસંદ કરો. એક strategy માટે replay ચલાવો અથવા **Compare Five Strategies** દબાવો. **Walk-forward Validation** માટે ચારથી નવ તારીખનું આવરણ જરૂરી છે.
5. અંતિમ holdout માટે અગાઉનો training replay પસંદ કરો, અલગ તારીખો આપો અને **Seal Final Holdout** દબાવો. Risk Manager **Sealed Holdouts**માંથી તેને એક વખત ચલાવી શકે છે.
6. **Virtual replay accounts**માં ઐતિહાસિક simulated postings દેખાય છે. **NO TRADE** એટલે જરૂરી પુરાવા અથવા પરવાનગીના અભાવે કોઈ વ્યવહારયોગ્ય signal આપવામાં આવ્યો નથી. આ આવૃત્તિમાં ચકાસેલું live feed કે prospective paper performance ઉપલબ્ધ નથી.
7. હોટસ્પોટ બંધ થાય તો offline પરીક્ષણ ચાલુ રાખી શકો છો. બ્રોકર માટે **Sync History**માં કારણ જુઓ. કનેક્શન અને પરવાનગી પાછાં મળે ત્યાર પછી **Historical Sync Plans**માં આગળનું સત્ર ચલાવો. જૂના ભાવને live quote તરીકે વાપરશો નહીં.

હાલના offline અભ્યાસ માટે બહારનું ખાતું, static IP કે subscription લેવાની જરૂર નથી. વાસ્તવિક ડેટા માટે સંબંધિત સ્રોતના ઉપયોગ અને સંગ્રહની મંજૂરી જરૂરી છે.
