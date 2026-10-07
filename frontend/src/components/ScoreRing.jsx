// Circular gauge showing the overall match score (0-100).
export default function ScoreRing({ score, label }) {
  const radius = 84;
  const circumference = 2 * Math.PI * radius;
  const filled = (Math.max(0, Math.min(100, score)) / 100) * circumference;

  return (
    <div className="ring">
      <svg width="200" height="200" viewBox="0 0 200 200" aria-label={`Match score ${score} percent`}>
        <defs>
          <linearGradient id="ringGradient" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor="#22D3EE" />
            <stop offset="0.6" stopColor="#A78BFA" />
            <stop offset="1" stopColor="#F472B6" />
          </linearGradient>
        </defs>
        <circle cx="100" cy="100" r={radius} fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth="18" />
        <circle
          className="ring-progress"
          cx="100"
          cy="100"
          r={radius}
          fill="none"
          stroke="url(#ringGradient)"
          strokeWidth="18"
          strokeLinecap="round"
          strokeDasharray={`${filled} ${circumference}`}
          transform="rotate(-90 100 100)"
        />
      </svg>
      <div className="ring-text">
        <span className="ring-score">{score}%</span>
        <span className="ring-label">{label}</span>
      </div>
    </div>
  );
}
