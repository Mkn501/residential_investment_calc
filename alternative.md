**[NEW] Alternative UI** 

--- html ---

import React, { useState, useEffect } from 'react';
import { Calculator, Scale, AlertTriangle, TrendingDown, TrendingUp, CheckCircle, Info, Home, PieChart } from 'lucide-react';

const Card = ({ children, className = "" }) => (
  <div className={`bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden ${className}`}>
    {children}
  </div>
);

const SectionTitle = ({ icon: Icon, title }) => (
  <div className="flex items-center gap-2 mb-4 text-slate-800">
    <Icon className="w-5 h-5 text-blue-600" />
    <h2 className="text-lg font-bold">{title}</h2>
  </div>
);

const InputGroup = ({ label, value, onChange, unit = "€", step = "100", type = "number", helpText = "" }) => (
  <div className="mb-3">
    <label className="block text-xs font-medium text-slate-500 uppercase tracking-wide mb-1">
      {label}
    </label>
    <div className="relative">
      <input
        type={type}
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value) || 0)}
        className="w-full pl-3 pr-8 py-2 bg-slate-50 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all font-mono text-slate-700"
      />
      <span className="absolute right-3 top-2 text-slate-400 text-sm">{unit}</span>
    </div>
    {helpText && <p className="text-xs text-slate-400 mt-1">{helpText}</p>}
  </div>
);

const ResultRow = ({ label, value, subValue, highlight = false, negative = false }) => (
  <div className={`flex justify-between items-end py-2 border-b border-slate-100 last:border-0 ${highlight ? 'bg-blue-50 -mx-4 px-4 py-3 rounded-lg' : ''}`}>
    <span className={`text-sm ${highlight ? 'font-semibold text-blue-900' : 'text-slate-600'}`}>{label}</span>
    <div className="text-right">
      <div className={`font-mono font-medium ${negative ? 'text-red-600' : highlight ? 'text-blue-700' : 'text-slate-800'}`}>
        {value}
      </div>
      {subValue && <div className="text-xs text-slate-400">{subValue}</div>}
    </div>
  </div>
);

export default function App() {
  const [activeTab, setActiveTab] = useState('calculator');

  // --- STATE: INPUTS ---
  const [purchasePrice, setPurchasePrice] = useState(469000);
  const [size, setSize] = useState(90);
  
  // Kaufnebenkosten (Standard Bayern)
  const [maklerPercent, setMaklerPercent] = useState(3.57);
  const [taxPercent, setTaxPercent] = useState(3.5);
  const [notaryPercent, setNotaryPercent] = useState(2.0);

  // Miete & Kosten
  const [currentRent, setCurrentRent] = useState(900);
  const [nonRecoverableCosts, setNonRecoverableCosts] = useState(80);
  
  // Finanzierung
  const [equityPercent, setEquityPercent] = useState(20);
  const [interestRate, setInterestRate] = useState(3.8);

  // Benchmarks
  const [bondYield, setBondYield] = useState(2.8);
  const [targetYield, setTargetYield] = useState(3.0);

  // --- DERIVED CALCULATIONS ---
  const ancillaryCostPercent = maklerPercent + taxPercent + notaryPercent;
  const ancillaryCosts = purchasePrice * (ancillaryCostPercent / 100);
  const totalInvest = purchasePrice + ancillaryCosts;
  
  const equity = totalInvest * (equityPercent / 100);
  const loanAmount = totalInvest - equity;
  const yearlyInterest = loanAmount * (interestRate / 100);

  // Rent Scenarios
  const maxRentIncrease = currentRent * 1.15; // 15% Cap
  
  const annualRentCurrent = currentRent * 12;
  const annualRentPotential = maxRentIncrease * 12;
  
  const annualCosts = nonRecoverableCosts * 12;

  // Yields (Netto-Mietrendite auf Gesamtinvest)
  const netYieldCurrent = ((annualRentCurrent - annualCosts) / totalInvest) * 100;
  const netYieldPotential = ((annualRentPotential - annualCosts) / totalInvest) * 100;

  // Cashflow (Pre-Tax)
  const cashflowCurrent = annualRentCurrent - annualCosts - yearlyInterest;
  const cashflowPotential = annualRentPotential - annualCosts - yearlyInterest;
  
  // Return on Equity
  const roeCurrent = (cashflowCurrent / equity) * 100;

  // Bond Comparison
  const bondReturn = equity * (bondYield / 100); // Risk-free return on the equity cash

  // Reverse Calculation (Target Price)
  const maxTotalInvestForTarget = annualRentPotential / (targetYield / 100);
  const maxPurchasePriceForTarget = maxTotalInvestForTarget / (1 + (ancillaryCostPercent / 100));
  const priceDifference = purchasePrice - maxPurchasePriceForTarget;

  // Formatting Helper
  const fmt = (num) => new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }).format(num);
  const fmtPct = (num) => new Intl.NumberFormat('de-DE', { maximumFractionDigits: 2 }).format(num) + " %";

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 font-sans pb-12">
      
      {/* HEADER */}
      <header className="bg-slate-900 text-white py-6 shadow-lg">
        <div className="max-w-5xl mx-auto px-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="bg-blue-600 p-2 rounded-lg">
              <Scale className="text-white w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight">Immo-Klartext</h1>
              <p className="text-slate-400 text-sm">Der Realitäts-Check für Ihre Kapitalanlage</p>
            </div>
          </div>
          
          <nav className="hidden md:flex bg-slate-800 rounded-lg p-1">
            {[
              { id: 'calculator', label: 'Rendite & Cashflow', icon: Calculator },
              { id: 'reverse', label: 'Wunsch-Preis', icon: TrendingUp },
              { id: 'checklist', label: 'Due Diligence', icon: CheckCircle },
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all ${
                  activeTab === tab.id 
                    ? 'bg-blue-600 text-white shadow-sm' 
                    : 'text-slate-400 hover:text-white hover:bg-slate-700'
                }`}
              >
                <tab.icon className="w-4 h-4" />
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </header>
      
      {/* MOBILE NAV */}
      <div className="md:hidden flex overflow-x-auto gap-2 p-2 bg-white border-b border-slate-200 sticky top-0 z-10">
        {[{ id: 'calculator', label: 'Rendite' }, { id: 'reverse', label: 'Ziel-Preis' }, { id: 'checklist', label: 'Checkliste' }].map(tab => (
           <button
             key={tab.id}
             onClick={() => setActiveTab(tab.id)}
             className={`px-4 py-2 rounded-full text-sm whitespace-nowrap ${activeTab === tab.id ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-600'}`}
           >
             {tab.label}
           </button>
        ))}
      </div>

      <main className="max-w-5xl mx-auto px-4 mt-8">
        
        {/* --- TAB: CALCULATOR --- */}
        {activeTab === 'calculator' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* INPUTS LEFT COLUMN */}
            <div className="lg:col-span-1 space-y-6">
              <Card className="p-5">
                <SectionTitle icon={Home} title="Objekt & Kosten" />
                <InputGroup label="Kaufpreis" value={purchasePrice} onChange={setPurchasePrice} />
                <InputGroup label="Wohnfläche (m²)" value={size} onChange={setSize} unit="m²" step="1" />
                
                <div className="grid grid-cols-3 gap-2">
                  <InputGroup label="Makler (%)" value={maklerPercent} onChange={setMaklerPercent} unit="%" step="0.1" />
                  <InputGroup label="Grunderwerb (%)" value={taxPercent} onChange={setTaxPercent} unit="%" step="0.1" />
                  <InputGroup label="Notar (%)" value={notaryPercent} onChange={setNotaryPercent} unit="%" step="0.1" />
                </div>
                
                <div className="mt-4 pt-4 border-t border-slate-100">
                  <div className="flex justify-between text-sm text-slate-500 mb-1">
                    <span>Kaufnebenkosten:</span>
                    <span>{fmt(ancillaryCosts)}</span>
                  </div>
                  <div className="flex justify-between font-bold text-slate-800">
                    <span>Gesamtinvestition:</span>
                    <span>{fmt(totalInvest)}</span>
                  </div>
                </div>
              </Card>

              <Card className="p-5">
                <SectionTitle icon={PieChart} title="Miete & Finanzierung" />
                <InputGroup label="Aktuelle Kaltmiete" value={currentRent} onChange={setCurrentRent} />
                <InputGroup label="Nicht umlegbare Kosten" value={nonRecoverableCosts} onChange={setNonRecoverableCosts} helpText="Verwaltung + Rücklagen" />
                
                <div className="h-px bg-slate-100 my-4" />
                
                <InputGroup label="Zinssatz Bank" value={interestRate} onChange={setInterestRate} unit="%" step="0.1" />
                <InputGroup label="Eigenkapital-Anteil" value={equityPercent} onChange={setEquityPercent} unit="%" step="5" />
                
                <div className="text-xs text-slate-400 mt-2">
                  Darlehenssumme: {fmt(loanAmount)} <br/>
                  Eigenkapital: {fmt(equity)}
                </div>
              </Card>
            </div>

            {/* RESULTS RIGHT COLUMN */}
            <div className="lg:col-span-2 space-y-6">
              
              {/* STATUS QUO VS POTENTIAL */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* CURRENT SCENARIO */}
                <Card className="p-5 border-t-4 border-t-slate-400">
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="font-bold text-slate-700">Status Quo (Aktuell)</h3>
                    <span className="bg-slate-100 text-slate-600 px-2 py-1 rounded text-xs font-mono">{fmt(currentRent)}/Mo</span>
                  </div>
                  
                  <div className="space-y-4">
                    <div>
                      <div className="text-slate-500 text-xs uppercase">Netto-Mietrendite</div>
                      <div className="text-3xl font-bold text-slate-700">{fmtPct(netYieldCurrent)}</div>
                    </div>
                    
                    <div className="space-y-2">
                      <ResultRow label="Reinertrag (p.a.)" value={fmt(annualRentCurrent - annualCosts)} />
                      <ResultRow label="Zinskosten" value={`- ${fmt(yearlyInterest)}`} negative />
                      <ResultRow 
                        label="Cashflow (vor Steuer)" 
                        value={fmt(cashflowCurrent)} 
                        subValue={fmt(cashflowCurrent/12) + " / Monat"}
                        highlight 
                        negative={cashflowCurrent < 0} 
                      />
                    </div>
                  </div>
                </Card>

                {/* POTENTIAL SCENARIO */}
                <Card className="p-5 border-t-4 border-t-blue-500 bg-blue-50/30">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="font-bold text-blue-900">Nach 15% Erhöhung</h3>
                      <p className="text-xs text-blue-600 mt-1">Kappungsgrenze beachten!</p>
                    </div>
                    <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs font-mono font-bold">{fmt(maxRentIncrease)}/Mo</span>
                  </div>
                  
                  <div className="space-y-4">
                    <div>
                      <div className="text-blue-600/70 text-xs uppercase">Netto-Mietrendite</div>
                      <div className="text-3xl font-bold text-blue-600">{fmtPct(netYieldPotential)}</div>
                    </div>
                    
                    <div className="space-y-2">
                      <ResultRow label="Reinertrag (p.a.)" value={fmt(annualRentPotential - annualCosts)} />
                      <ResultRow label="Zinskosten" value={`- ${fmt(yearlyInterest)}`} negative />
                      <ResultRow 
                        label="Cashflow (vor Steuer)" 
                        value={fmt(cashflowPotential)} 
                        subValue={fmt(cashflowPotential/12) + " / Monat"}
                        highlight 
                        negative={cashflowPotential < 0} 
                      />
                    </div>
                  </div>
                </Card>
              </div>

              {/* COMPARISON BAR */}
              <Card className="p-6 bg-gradient-to-br from-slate-900 to-slate-800 text-white border-none">
                <div className="flex items-start gap-4 mb-6">
                  <div className="p-3 bg-white/10 rounded-lg">
                    <Scale className="w-6 h-6 text-yellow-400" />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold">Der harte Vergleich: Ihr Eigenkapital ({fmt(equity)})</h3>
                    <p className="text-slate-400 text-sm">Was passiert mit Ihrem Geld im ersten Jahr?</p>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-8">
                  {/* OPTION A: IMMO */}
                  <div className="relative">
                    <div className="flex justify-between mb-2 text-sm font-medium">
                      <span className="text-slate-300">Option A: Diese Immobilie</span>
                      <span className={cashflowPotential < 0 ? "text-red-400" : "text-green-400"}>{fmt(cashflowPotential)}</span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-3 mb-1 overflow-hidden">
                       {cashflowPotential > 0 ? (
                         <div className="bg-green-500 h-3 rounded-full" style={{ width: `${Math.min((cashflowPotential / 5000) * 100, 100)}%` }}></div>
                       ) : (
                         <div className="bg-red-500 h-3 rounded-full w-full opacity-50"></div> // Visual indicator for loss
                       )}
                    </div>
                    <p className="text-xs text-slate-400 mt-2">
                      {cashflowPotential < 0 
                        ? `Achtung: Negativer Hebel! Sie verlieren jährlich ${fmtPct(Math.abs(roeCurrent))} Ihres Eigenkapitals.` 
                        : "Positiver Cashflow."}
                    </p>
                  </div>

                  {/* OPTION B: BOND */}
                  <div>
                    <div className="flex justify-between mb-2 text-sm font-medium">
                      <span className="text-slate-300">Option B: Bundesanleihe ({bondYield}%)</span>
                      <span className="text-green-400">+{fmt(bondReturn)}</span>
                    </div>
                    <div className="w-full bg-slate-700 rounded-full h-3 mb-1">
                      <div className="bg-yellow-400 h-3 rounded-full" style={{ width: '100%' }}></div>
                    </div>
                    <p className="text-xs text-slate-400 mt-2">
                      Garantierter Ertrag ohne Arbeit, Risiko oder Instandhaltung.
                    </p>
                  </div>
                </div>

                {/* VERDICT */}
                <div className="mt-8 pt-6 border-t border-white/10 flex gap-3 items-center">
                   {bondReturn > cashflowPotential ? (
                     <>
                      <AlertTriangle className="text-red-400 w-5 h-5 flex-shrink-0" />
                      <p className="text-sm font-medium text-red-200">
                        Fazit: Die risikolose Anleihe schlägt das Immobilien-Investment aktuell um <span className="text-white font-bold underline">{fmt(bondReturn - cashflowPotential)}</span> pro Jahr.
                      </p>
                     </>
                   ) : (
                     <>
                      <CheckCircle className="text-green-400 w-5 h-5 flex-shrink-0" />
                      <p className="text-sm font-medium text-green-200">
                        Fazit: Die Immobilie erwirtschaftet mehr Cashflow als die Anleihe.
                      </p>
                     </>
                   )}
                </div>
              </Card>

            </div>
          </div>
        )}

        {/* --- TAB: REVERSE CALC --- */}
        {activeTab === 'reverse' && (
          <div className="max-w-3xl mx-auto">
            <Card className="p-8">
              <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-slate-800 mb-2">Rückwärts-Rechner</h2>
                <p className="text-slate-500">
                  Wenn die Miete gedeckelt ist (auf {fmt(maxRentIncrease)}), wie viel darf die Wohnung maximal kosten, 
                  um Ihre Wunsch-Rendite zu erzielen?
                </p>
              </div>

              <div className="bg-blue-50 p-6 rounded-xl flex flex-col md:flex-row items-center justify-between gap-6 mb-8">
                <div className="flex-1 w-full">
                  <label className="text-xs font-bold text-blue-800 uppercase mb-2 block">Ihre Wunsch-Rendite (%)</label>
                  <input 
                    type="range" 
                    min="2" 
                    max="6" 
                    step="0.1" 
                    value={targetYield} 
                    onChange={(e) => setTargetYield(parseFloat(e.target.value))}
                    className="w-full h-2 bg-blue-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                  />
                  <div className="flex justify-between text-xs text-blue-600 mt-2 font-mono">
                    <span>2%</span>
                    <span className="font-bold text-lg">{targetYield}%</span>
                    <span>6%</span>
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <div className="flex justify-between items-center py-4 border-b border-slate-100">
                   <span className="text-slate-600">Maximales Gesamtinvest ("All-in"):</span>
                   <span className="font-mono text-xl font-medium text-slate-700">{fmt(maxTotalInvestForTarget)}</span>
                </div>
                <div className="flex justify-between items-center py-4 border-b border-slate-100">
                   <span className="text-slate-500 text-sm">Davon Kaufnebenkosten ({ancillaryCostPercent}%):</span>
                   <span className="font-mono text-slate-500">-{fmt(maxTotalInvestForTarget - maxPurchasePriceForTarget)}</span>
                </div>
                
                <div className="flex justify-between items-center bg-green-50 p-4 rounded-lg mt-4 border border-green-100">
                   <span className="font-bold text-green-900 text-lg">Fairer Kaufpreis:</span>
                   <span className="font-mono text-3xl font-bold text-green-700">{fmt(maxPurchasePriceForTarget)}</span>
                </div>
              </div>

              <div className="mt-8 p-4 bg-red-50 border border-red-100 rounded-lg text-center">
                 <p className="text-red-800 font-medium mb-1">Verhandlungspotenzial</p>
                 <p className="text-red-600 text-sm">
                   Die Wohnung ist aktuell um <span className="font-bold">{fmt(priceDifference)}</span> zu teuer für Ihre Renditeziele.
                 </p>
              </div>
            </Card>
          </div>
        )}

        {/* --- TAB: CHECKLIST --- */}
        {activeTab === 'checklist' && (
          <div className="max-w-3xl mx-auto space-y-6">
            <Card className="p-6 border-l-4 border-l-yellow-400">
              <SectionTitle icon={AlertTriangle} title="Die 'vergessenen' Risiken" />
              <p className="text-slate-600 mb-6">
                Bevor Sie investieren, müssen diese 5 Dokumente geprüft werden. Fehlt eines, ist der Kaufpreis eine "Black Box".
              </p>
              
              <ul className="space-y-4">
                {[
                  { title: "Eigentümer-Protokolle (letzte 3 Jahre)", desc: "Gibt es Streit? Sind teure Sanierungen (Dach, Fassade) geplant, die nicht im Exposé stehen?" },
                  { title: "Rücklagen-Stand (Gesamt & Anteil)", desc: "Ist genug Geld da, wenn die Heizung (1992!) morgen ausfällt? Droht Sonderumlage?" },
                  { title: "Heizungs-Typ & Energieausweis", desc: "Handelt es sich um einen Niedertemperaturkessel (Bestandsschutz) oder Standardkessel (Austauschpflicht)? GEG beachten!" },
                  { title: "Teilungserklärung", desc: "Wer zahlt die Fenster? Gemeinschaft oder Sie allein? Was ist Sondereigentum?" },
                  { title: "Mietkonto & Historie", desc: "Zahlt der Mieter pünktlich? Gibt es Rückstände? Eigenbedarf geplant (Härtefall-Risiko bei Familie)?" }
                ].map((item, idx) => (
                  <li key={idx} className="flex gap-4 items-start">
                    <div className="bg-slate-100 text-slate-500 font-bold w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0 text-xs mt-0.5">
                      {idx + 1}
                    </div>
                    <div>
                      <h4 className="font-bold text-slate-800">{item.title}</h4>
                      <p className="text-sm text-slate-500 leading-relaxed">{item.desc}</p>
                    </div>
                  </li>
                ))}
              </ul>
            </Card>
            
            <div className="text-center text-sm text-slate-400 pt-8">
              <p>Disclaimer: Diese Berechnung dient der Information und stellt keine Steuer- oder Anlageberatung dar.</p>
            </div>
          </div>
        )}

      </main>
    </div>
  );
}

--- html ---