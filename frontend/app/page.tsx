import styles from './page.module.css'
import Link from 'next/link'

export default function HomePage() {
  return (
    <div className={styles.shell}>
      {/* Hero */}
      <section className={styles.hero}>
        <div className={styles.heroGlow} />
        <div className={styles.container}>
          <p className={styles.kicker}>Cloud built for scale</p>
          <h1 className={styles.title}>Deploy lightning‑fast, stay infinitely scalable.</h1>
          <p className={styles.subtitle}>
            Web hosting, VPS, game servers, domains, and SSL — engineered for speed, security, and reliability.
          </p>
          <div className={styles.ctaRow}>
            <Link href="#get-started" className={styles.ctaPrimary}>Get Started</Link>
            <Link href="#pricing" className={styles.ctaSecondary}>View Pricing</Link>
          </div>
          <div className={styles.heroStats}>
            <div>
              <span className={styles.stat}>99.99%</span>
              <span className={styles.statLabel}>Uptime SLA</span>
            </div>
            <div>
              <span className={styles.stat}>&lt;50ms</span>
              <span className={styles.statLabel}>Global latency</span>
            </div>
            <div>
              <span className={styles.stat}>24/7</span>
              <span className={styles.statLabel}>Expert support</span>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className={styles.section} id="features">
        <div className={styles.container}>
          <h2 className={styles.sectionTitle}>Built for modern workloads</h2>
          <p className={styles.sectionSubtitle}>Fast. Secure. Scalable. Everything you need to ship with confidence.</p>
          <div className={styles.grid3}>
            <FeatureCard icon="⚡" title="Fast" desc="NVMe storage, edge CDN, and global Anycast network for sub‑50ms responses." />
            <FeatureCard icon="🛡️" title="Secure" desc="DDoS protection, auto‑patching, managed firewalls, and free SSL on every plan." />
            <FeatureCard icon="📈" title="Scalable" desc="From hobby projects to planet‑scale apps with autoscaling and zero‑downtime deploys." />
          </div>
        </div>
      </section>

      {/* Pricing teaser */}
      <section className={styles.section} id="pricing">
        <div className={styles.container}>
          <h2 className={styles.sectionTitle}>Transparent pricing</h2>
          <p className={styles.sectionSubtitle}>Simple tiers that grow with you. No surprise bills.</p>
          <div className={styles.grid3}>
            <PriceCard tier="Starter" price="$5/mo" features={["1 project", "Shared CPU", "Free SSL", "Basic support"]} />
            <PriceCard tier="Pro" price="$20/mo" highlight features={["Unlimited projects", "Dedicated vCPU", "Global CDN", "Priority support"]} />
            <PriceCard tier="Scale" price="Custom" features={["Clusters", "Autoscaling", "Private networking", "SLA & SSO"]} />
          </div>
        </div>
      </section>

      {/* Why Stralix */}
      <section className={styles.sectionAlt} id="why">
        <div className={styles.container}>
          <h2 className={styles.sectionTitle}>Why Stralix</h2>
          <div className={styles.grid2}> 
            <ul className={styles.bullets}>
              <li><span>Global edge network with smart routing</span></li>
              <li><span>One‑click SSL, domains, and zero‑downtime deploys</span></li>
              <li><span>Developer‑first: APIs, logs, metrics, and CLI</span></li>
              <li><span>Battle‑tested reliability and security by default</span></li>
            </ul>
            <div className={styles.calloutCard}>
              <h3>Bring your stack.</h3>
              <p>Next.js, Node, containers, game servers — if it builds, it ships. Connect your repo and go live.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className={styles.finalCta} id="get-started">
        <div className={styles.container}>
          <h2>Launch in minutes.</h2>
          <p>Start free, scale on demand, and pay only for what you use.</p>
          <div className={styles.ctaRowCenter}>
            <Link href="#" className={styles.ctaPrimary}>Create account</Link>
            <Link href="#" className={styles.ctaSecondary}>Talk to sales</Link>
          </div>
        </div>
      </section>
    </div>
  )
}

function FeatureCard({ icon, title, desc }: { icon: string; title: string; desc: string }) {
  return (
    <div className={styles.cardFeature}>
      <div className={styles.featureIcon}>{icon}</div>
      <h3>{title}</h3>
      <p>{desc}</p>
    </div>
  )
}

function PriceCard({ tier, price, features, highlight }: { tier: string; price: string; features: string[]; highlight?: boolean }) {
  return (
    <div className={highlight ? `${styles.cardPrice} ${styles.cardPriceHighlight}` : styles.cardPrice}>
      <div className={styles.priceHead}>
        <h3>{tier}</h3>
        <span className={styles.price}>{price}</span>
      </div>
      <ul className={styles.priceList}>
        {features.map((f) => (
          <li key={f}>{f}</li>
        ))}
      </ul>
      <button className={styles.ctaSmall}>Choose {tier}</button>
    </div>
  )
}
