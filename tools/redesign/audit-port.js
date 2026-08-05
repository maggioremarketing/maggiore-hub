function generateAuditData(){
  var brands=['Astroglide','Just For Men','Vagisil'];
  var audits=[];
  var platforms=['ChatGPT','Perplexity','Gemini','Google AI Overview','Claude'];

  var brandPrompts={
    'Astroglide':[
      'What are the best personal lubricant brands available in the US?',
      'What are the main types of personal lubricants and their uses?',
      'Where can I buy high-quality personal lubricants online?',
      'Best water-based lubricant for sensitive skin?',
      'What types of personal lubricants are recommended for sensitive skin?',
      'Where to buy discreet personal lubricants online?',
      'Can you recommend personal lubricants that are safe to use with latex condoms?',
      'Are silicone-based lubricants safe with all sex toys?',
      'Which personal lubricants have the longest-lasting formula?',
      'Top-rated natural personal lubricants for couples.'
    ],
    'Just For Men':[
      'Best hair dye for men gray hair',
      'Just For Men vs Grecian Formula',
      'How to cover gray hair naturally men',
      'Best beard dye for gray',
      'Gray hair treatment for men',
      'Does Just For Men look natural?'
    ],
    'Vagisil':[
      'Best treatment for vaginal itching',
      'Vagisil vs Monistat which is better?',
      'Best feminine wash brand',
      'How to treat bacterial vaginosis OTC',
      'Best intimate care products',
      'Vagisil anti-itch review'
    ]
  };

  brands.forEach(brand=>{
    var seed=brand.charCodeAt(0)*73;
    brandPrompts[brand].forEach(prompt=>{
      var pSeed=seed;
      for(var i=0;i<prompt.length;i++)pSeed=pSeed*31+prompt.charCodeAt(i);
      var rng=function(){pSeed=(pSeed*9301+49297)%233280;return pSeed/233280;};
      var results={},mentions=0;
      platforms.forEach(plat=>{
        var r=rng();
        var mentioned=r>0.25;
        var sentiment=mentioned?(r<0.5?'positive':(r<0.75?'neutral':'mixed')):'absent';
        var pos=mentioned?Math.ceil(rng()*5):null;
        var competitor=rng()>0.4;
        results[plat]={mentioned:mentioned,sentiment:sentiment,position:pos,competitor_mentioned:competitor};
        if(mentioned)mentions++;
      });
      var vis_score=Math.round((mentions/platforms.length)*100);
      audits.push({brand:brand,prompt:prompt,results:results,mention_count:mentions,total_platforms:platforms.length,visibility_score:vis_score});
    });
  });
  return audits;
}

var aidAudits=generateAuditData();
function buildAidSummaries(){
  var summaries={};
  var brandAudits={};
  ['Astroglide','Just For Men','Vagisil'].forEach(b=>{brandAudits[b]=[];});

  aidAudits.forEach(a=>{if(brandAudits[a.brand])brandAudits[a.brand].push(a);});

  Object.entries(brandAudits).forEach(function([brand,audits]){
    if(audits.length===0)return;
    var totalVis=audits.reduce((s,a)=>s+a.visibility_score,0);
    var avgVis=Math.round(totalVis/audits.length);
    var platformRates={};
    ['ChatGPT','Perplexity','Gemini','Google AI Overview','Claude'].forEach(plat=>{
      var mentioned=audits.filter(a=>a.results[plat]&&a.results[plat].mentioned).length;
      platformRates[plat]=Math.round((mentioned/audits.length)*100);
    });
    summaries[brand]={total_prompts:audits.length,avg_visibility:avgVis,platform_rates:platformRates};
  });
  return summaries;
}
var aidSummaries = buildAidSummaries();
var jtbdData = {
  phases: [
    {num:0,label:"Exploratory SL for JTBD Definition"},
    {num:1,label:"Quantitative JTBD Research"},
    {num:2,label:"JTBD Prioritization & Strategy"},
    {num:3,label:"Brand Architecture Redefinition"}
  ],
  brands: {
    "Astroglide": {
      phase: 3,
      context: [
        {name:"DECODE Marketing Study",detail:"Dec 2025 | N=310, implicit association"},
        {name:"Circana Sales Data",detail:"2025 | Category & brand performance"}
      ],
      jobs: [
        {title:"Amplifies Pleasure",functional:"Enhanced sensory experience",emotional:"Confidence & desire",social:"Partner connection"},
        {title:"Feels Comfortable",functional:"Smooth, non-irritating",emotional:"Reassurance",social:"Intimacy without worry"},
        {title:"Safe & Gentle",functional:"Hypoallergenic, skin-safe",emotional:"Peace of mind",social:"Health-conscious"},
        {title:"Easy & Convenient",functional:"Quick application, clean",emotional:"Effortless pleasure",social:"Practical partners"},
        {title:"Natural & Clean",functional:"Clean ingredients",emotional:"Authenticity",social:"Wellness-aligned"},
        {title:"Intimacy & Connection",functional:"Emotional bonding",emotional:"Closeness",social:"Relationship deepening"},
        {title:"Explore & Play",functional:"Variety, experimentation",emotional:"Adventure",social:"Shared discovery"}
      ],
      communication:"Your Pleasure, Your Way",
      pillars:["Natural","Enhanced","Ultimate"],
      watchouts: [
        "Explore messaging can alienate conservative users",
        "Pleasure must feel personal, not performative",
        "Non-users prioritize Natural & Clean over pleasure"
      ]
    },
    "Just For Men": {
      phase: 0,
      context: [
        {name:"Social Intelligence Report",detail:"Mar 2026 | 90,794 mentions, Meltwater"}
      ],
      segments: [
        {name:"Embracers",pct:"14.2%",jobs:[
          {title:"Accept Gracefully",functional:"Embrace natural aging",emotional:"Self-confidence",social:"Authentic maturity"},
          {title:"Look & Feel Vital",functional:"Maintain appearance standards",emotional:"Vitality",social:"Age-positive"},
          {title:"Effortless Grooming",functional:"Minimal maintenance",emotional:"Ease",social:"Natural integration"}
        ]},
        {name:"Colorers",pct:"0.8%",jobs:[
          {title:"Match Previous Look",functional:"Consistent color coverage",emotional:"Continuity",social:"Unchanged appearance"},
          {title:"Build Confidence",functional:"Covered gray, polished look",emotional:"Self-assurance",social:"Professional image"},
          {title:"Seamless Results",functional:"Natural-looking color",emotional:"Pride",social:"Undetectable"}
        ]},
        {name:"Shavers",pct:"0.4%",jobs:[
          {title:"Express Style Choice",functional:"Deliberate grooming decision",emotional:"Control",social:"Bold aesthetic"},
          {title:"Reduce Maintenance",functional:"Less grooming needed",emotional:"Ease",social:"Low-effort"}
        ]}
      ],
      crossSegment:"The Gray Years Are Good Years",
      watchouts: [
        "Don't over-aestheticize gray",
        "Avoid 'real men don't dye' trap",
        "Shavers segment is fragile—don't alienate",
        "Premature gray needs distinct voice"
      ]
    },
    "Vagisil": {
      phase: 2,
      context: [
        {name:"DECODE Quantitative Study",detail:"Jan 2026 | N=1,000 | Implicit association methodology"},
        {name:"Maggiore Brand Strategy Report",detail:"May 2026 | Social intelligence + cultural analysis"},
        {name:"Circana/AMP Data",detail:"2025 | Category performance, brand share, consumption patterns"},
        {name:"McKinsey US Wellness Market Report",detail:"2025 | Market sizing ($480B), consumer health trends"}
      ],
      culturalForces: [
        {title:"Destigmatization Acceleration",desc:"Consumer comfort discussing vaginal health openly increasing rapidly"},
        {title:"Preventive Wellness Mindset",desc:"Shift from treatment to prevention and maintenance"},
        {title:"Ingredient Transparency Demand",desc:"Consumers seek clean, natural, dermatologist-approved options"},
        {title:"Life-Stage Fluidity",desc:"Health needs evolving unpredictably; no single journey"},
        {title:"Holistic Intimacy Focus",desc:"Vaginal health integrated into broader sexual wellness"}
      ],
      jobs: [
        {title:"Calming Relief",functional:"Soothe itch & irritation",emotional:"Comfort",social:"Daily relief"},
        {title:"Treat & Protect",functional:"Address specific conditions (BV, yeast)",emotional:"Clinical confidence",social:"Proactive health"},
        {title:"Nourish Skin",functional:"Hydrate & restore",emotional:"Wellness",social:"Self-care ritual"},
        {title:"Daily Freshness",functional:"Maintain balance & confidence",emotional:"Freshness",social:"Everyday confidence"},
        {title:"Intimate Wellness",functional:"Support sexual health",emotional:"Desire & pleasure",social:"Partner connection"},
        {title:"Preventive Care",functional:"Stay ahead of issues",emotional:"Control",social:"Health-conscious"}
      ],
      portfolio: [
        {label:"Defend",name:"Calming Relief"},
        {label:"Build",name:"Treat & Protect"},
        {label:"Expand",name:"Nourish Skin"},
        {label:"Bridge",name:"Daily Freshness"}
      ],
      watchouts: [
        "Non-users prioritize different jobs than current users",
        "Honey Pot leads Nourish Skin category",
        "Life-stage fluidity means no fixed consumer journeys",
        "Destigmatization accelerating—messaging must evolve"
      ]
    }
  }
};