const AGENTS = [
  { key: 'planner',    label: 'Planner',    icon: '📋', color: '#6366F1', x: 80,  y: 180 },
  { key: 'retriever',  label: 'Retriever',  icon: '🔍', color: '#3B82F6', x: 180, y: 180 },
  { key: 'analyst',    label: 'Analyst',    icon: '🧠', color: '#8B5CF6', x: 280, y: 180 },
  { key: 'strategist', label: 'Strategist', icon: '♟️', color: '#10B981', x: 380, y: 180 },
  { key: 'generator',  label: 'Generator',  icon: '⚙️', color: '#F59E0B', x: 480, y: 180 },
  { key: 'evaluator',  label: 'Evaluator',  icon: '⚖️', color: '#EF4444', x: 480, y: 280 },
];

const EDGES = [
  { from: 'planner',    to: 'retriever' },
  { from: 'retriever',  to: 'analyst' },
  { from: 'analyst',    to: 'strategist' },
  { from: 'strategist', to: 'generator' },
  { from: 'generator',  to: 'evaluator' }
];

function AgentNode({ agent, status }) {
  const isRunning = status === 'running';
  const isDone = status === 'completed';

  const color = isDone ? '#10B981' : isRunning ? agent.color : 'rgba(255,255,255,0.1)';
  const stroke = isDone ? '#10B981' : isRunning ? agent.color : 'rgba(255,255,255,0.2)';

  return (
    <g transform={`translate(${agent.x},${agent.y})`} className="transition-all duration-500">
      {isRunning && (
        <circle r="30" fill="none" stroke={agent.color} strokeWidth="1" opacity="0.5">
          <animate attributeName="r" from="22" to="35" dur="1.5s" repeatCount="indefinite" />
          <animate attributeName="opacity" from="0.5" to="0" dur="1.5s" repeatCount="indefinite" />
        </circle>
      )}
      
      <circle r="22" fill={color} stroke={stroke} strokeWidth={isRunning ? 3 : 1}
        className="transition-colors duration-500"
        style={{ filter: isRunning ? `drop-shadow(0 0 8px ${agent.color})` : 'none' }}
      />
      <text textAnchor="middle" dominantBaseline="middle" fontSize="16" y="1">{agent.icon}</text>
      
      <text textAnchor="middle" y="38" fontSize="10" fontWeight={isRunning || isDone ? "bold" : "normal"}
            fill={isDone ? '#10B981' : isRunning ? 'white' : 'rgba(255,255,255,0.4)'}>
        {agent.label}
      </text>

      {isDone && (
        <circle r="8" cx="15" cy="-15" fill="#10B981" stroke="#000" strokeWidth="1">
           <title>Terminé</title>
        </circle>
      )}
    </g>
  );
}

export default function AgentGraph({ agentStatuses = {} }) {
  const getStatus = (key) => agentStatuses[key] || 'idle';

  return (
    <div className="flex flex-col h-full w-full bg-gray-900/50">
      <div className="p-4 border-b border-white/5 flex justify-between items-center">
        <span className="text-xs font-bold uppercase tracking-wider text-gray-400">TARA Pipeline Status</span>
        <div className="flex gap-2">
            <div className="w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
        </div>
      </div>

      <div className="flex-1 flex items-center justify-center p-4">
        {/* On élargit la viewBox pour faire tenir les 6 agents */}
        <svg viewBox="0 0 560 360" className="w-full h-full max-w-[560px]">
          {EDGES.map((edge, i) => {
            const from = AGENTS.find(a => a.key === edge.from);
            const to = AGENTS.find(a => a.key === edge.to);
            const active = getStatus(edge.to) === 'running';

            return (
              <g key={i}>
                <line x1={from.x} y1={from.y} x2={to.x} y2={to.y} 
                  stroke="rgba(255,255,255,0.1)" strokeWidth="1" strokeDasharray="4 4" />
                {active && (
                  <circle r="3" fill="#6366F1">
                    <animateMotion path={`M ${from.x} ${from.y} L ${to.x} ${to.y}`} dur="1s" repeatCount="indefinite" />
                  </circle>
                )}
              </g>
            );
          })}
          {AGENTS.map(agent => (
            <AgentNode key={agent.key} agent={agent} status={getStatus(agent.key)} />
          ))}
        </svg>
      </div>
      
      <div className="p-4 border-t border-white/5 flex gap-4 text-[10px] text-gray-500 justify-center">
        <div className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-gray-700" /> Waiting</div>
        <div className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-indigo-500" /> Running</div>
        <div className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-green-500" /> Done</div>
      </div>
    </div>
  );
}