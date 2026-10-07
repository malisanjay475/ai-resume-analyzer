import ScoreRing from "./ScoreRing.jsx";

function Meter({ label, value, color }) {
  return (
    <div className="meter">
      <div className="meter-head">
        <span>{label}</span>
        <strong>{value === null ? "n/a" : `${value}%`}</strong>
      </div>
      <div className="meter-track">
        <div className="meter-fill" style={{ width: `${value ?? 0}%`, background: color }} />
      </div>
    </div>
  );
}

function Chips({ items, kind, empty }) {
  if (!items.length) return <p className="muted">{empty}</p>;
  return (
    <div className="chips">
      {items.map((skill) => (
        <span key={skill} className={`chip ${kind}`}>
          {skill}
        </span>
      ))}
    </div>
  );
}

export default function Results({ result }) {
  return (
    <div className="results">
      <section className="card score-card">
        <ScoreRing score={result.score} label={result.label} />
        <div className="meters">
          <Meter label="Skill coverage" value={result.skill_coverage} color="#22D3EE" />
          <Meter label="Text similarity (TF-IDF)" value={result.text_similarity} color="#A78BFA" />
          <p className="muted small">
            Score = 60% skill coverage + 40% text similarity · {result.word_count} words read
          </p>
        </div>
      </section>

      <section className="card">
        <h3>
          Matched skills <span className="count">{result.matched_skills.length}</span>
        </h3>
        <Chips items={result.matched_skills} kind="matched" empty="No skills from the job were found yet." />
        <h3>
          Missing skills <span className="count pink">{result.missing_skills.length}</span>
        </h3>
        <Chips items={result.missing_skills} kind="missing" empty="None. You cover every skill the job asks for!" />
      </section>

      <section className="card">
        <h3>Suggestions</h3>
        <ul className="tips">
          {result.suggestions.map((tip) => (
            <li key={tip}>{tip}</li>
          ))}
        </ul>
      </section>
    </div>
  );
}
