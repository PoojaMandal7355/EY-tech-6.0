import React from 'react'

const Features = () => {
  const agents = [
    {
      title: 'Research AI Agent',
      tagline: 'Evidence-based insights for any molecule, disease, or dosage form.',
      description: 'Searches clinical trials, publications, and scientific data. Summarizes mechanism of action & efficacy evidence, identifies safety issues and contraindications, highlights unmet needs & novel research angles.',
      bestFor: 'R&D, repurposing ideas, feasibility checks',
      icon: '🔬'
    },
    {
      title: 'Market Intelligence Agent',
      tagline: 'Understand market size, competitors, pricing, and demand dynamics.',
      description: 'Competitor landscape analysis, market size & CAGR projections, patent cliffs & upcoming opportunities, regulatory + geographic market entry insights.',
      bestFor: 'Strategy teams, portfolio planning',
      icon: '📊'
    },
    {
      title: 'Formulation & Technology Agent',
      tagline: 'Explore alternative dosage forms and value-added formulations.',
      description: 'Suggests novel dosage forms (ER, ODT, TD patches), identifies excipient compatibility, predicts formulation risks (solubility, stability), manufacturing considerations.',
      bestFor: 'F&D teams, value-added generics',
      icon: '💊'
    },
    {
      title: 'Safety & Pharmacovigilance Agent',
      tagline: 'Detect safety signals before they become risks.',
      description: 'Summarizes ADR reports, identifies drug–drug interactions, highlights boxed warnings & high-risk populations, provides benefit–risk analyses.',
      bestFor: 'PV teams, regulatory safety',
      icon: '🛡️'
    },
    {
      title: 'Regulatory Navigator Agent',
      tagline: 'Your guide to global regulatory pathways.',
      description: 'Explains FDA, EMA, CDSCO pathways, identifies required studies for 505(b)(2) or ANDA, provides documentation checklists, suggests fastest approval routes.',
      bestFor: 'Regulatory affairs, submissions',
      icon: '⚖️'
    },
    {
      title: 'Competitive Intelligence Agent',
      tagline: 'Track competitors, pipeline assets, and upcoming launches.',
      description: 'Monitors competitors\' filings & approvals, shows pipeline molecules & clinical phases, tracks ANDA/505(b)(2) submissions, alerts for new patents or expirations.',
      bestFor: 'Strategy, BD, portfolio teams',
      icon: '🎯'
    },
    {
      title: 'Medical Writing Agent',
      tagline: 'Converts complex research into clean, publication-ready documents.',
      description: 'Creates summaries, posters, slide decks. Converts conversation outputs into downloadable PDFs, helps draft protocols, reports, SOPs, provides citation formatting.',
      bestFor: 'Medical affairs, R&D documentation',
      icon: '✍️'
    },
    {
      title: 'Patent & IP Agent',
      tagline: 'Check novelty, avoid infringements, explore white-space opportunities.',
      description: 'Identifies existing patents around molecules, detects formulation/polymorph/method-of-use conflicts, provides freedom-to-operate analysis, suggests patentable differentiation areas.',
      bestFor: 'IP teams, innovation groups',
      icon: '📜'
    }
  ]

  return (
    <section id='features' className='w-full py-20 bg-gradient-to-b from-transparent to-white dark:from-[#242124] dark:to-[#000000] border-t-2 border-emerald-300 dark:border-transparent'>
      <div className='max-w-7xl mx-auto px-6'>
        <div className='text-center mb-16'>
          <h2 className='text-3xl md:text-4xl font-extrabold text-gray-900 dark:text-white mb-4'>
            AI Agents for Pharmaceutical Research
          </h2>
          <p className='text-lg text-gray-600 dark:text-gray-100 max-w-2xl mx-auto'>
            Specialized AI agents working together to accelerate your drug discovery and research workflows
          </p>
        </div>

        <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6'>
          {agents.map((agent, index) => (
            <div
              key={index}
              className='p-6 rounded-xl bg-gradient-to-br from-white to-gray-50 dark:from-[#1a1a1a] dark:to-[#0a0a0a] border border-gray-200 dark:border-gray-700 shadow-lg dark:shadow-2xl dark:shadow-black/50 hover:shadow-xl hover:shadow-emerald-500/20 dark:hover:shadow-emerald-500/30 transition-all duration-300 hover:scale-102'
            >
              <div className='text-4xl mb-3'>{agent.icon}</div>
              <h3 className='text-lg font-bold text-gray-900 dark:text-white mb-2'>
                {agent.title}
              </h3>
              <p className='text-sm text-emerald-600 dark:text-emerald-400 font-medium mb-3 italic'>
                {agent.tagline}
              </p>
              <p className='text-sm text-gray-600 dark:text-gray-300 mb-3 leading-relaxed'>
                {agent.description}
              </p>
              <p className='text-xs text-gray-500 dark:text-gray-400 font-semibold'>
                Best for: <span className='font-normal'>{agent.bestFor}</span>
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

export default Features
