import styles from './page.module.css'
import Link from 'next/link'

export default function HomePage() {
  return (
    <div className={styles.shell}>
      {/* Hero */}
      <section className={styles.hero}>
        <div className={styles.heroGlow} />
        <div className={styles.container}>
          <p className={styles.kicker}>Hosting built for speed</p>
          <h1 className={styles.title}>Deploy in seconds. Scale without limits.</h1>
          <p className={styles.subtitle}>Web hosting, VPS, and game servers with instant setup, low latency, and global locations.</p>
          <div className={styles.ctaRow}>
            <Link href="#get-started" className={styles.ctaPrimary}>Deploy in Seconds</Link>
            <Link href="#pricing" className={styles.ctaSecondary}>View Pricing</Link>
          </div>
        </div>
      </section>

      {/* Core Offerings */}
      <section className={styles.section} id="offerings">
        <div className={styles.container}>
          <h2 className={styles.sectionTitle}>Everything you need</h2>
          <p className={styles.sectionSubtitle}>Powerful infrastructure for builders and teams.</p>
          <div className={styles.grid3}> 
            <OfferingCard title="Web Hosting" desc="Fast, secure, and simple hosting for websites and apps." />
            <OfferingCard title="VPS Hosting" desc="Dedicated resources with full root access and NVMe performance." />
            <OfferingCard title="Game Servers" desc="Low‑latency servers with DDoS protection and instant setup." />
          </div>
        </div>
      </section>

      {/* Why Stralix */}
      <section className={styles.sectionAlt} id="why">
        <div className={styles.container}>
          <h2 className={styles.sectionTitle}>Why Stralix</h2>
          <ul className={styles.bullets6}>
            <li><span>Low latency worldwide</span></li>
            <li><span>Free DDoS protection</span></li>
            <li><span>Instant setup</span></li>
            <li><span>Global locations</span></li>
            <li><span>99.9% uptime SLA</span></li>
            <li><span>24/7 expert support</span></li>
          </ul>
        </div>
      </section>

      {/* Pricing Preview */}
      <section className={styles.section} id="pricing">
        <div className={styles.container}>
          <h2 className={styles.sectionTitle}>Simple, transparent pricing</h2>
          <p className={styles.sectionSubtitle}>Fair plans that scale with you. No surprise bills.</p>
          <div className={styles.grid3}>
            <PriceCard tier="Web Starter" price="$3.99/mo" features={["1 website", "Free SSL", "10GB SSD", "Basic support"]} />
            <PriceCard tier="VPS Pro" price="$12.99/mo" highlight features={["2 vCPU", "4GB RAM", "80GB NVMe", "Root access"]} />
            <PriceCard tier="Game Prime" price="$9.99/mo" features={["DDoS protected", "Low latency", "Instant deploy", "Mod support"]} />
          </div>
          <div className={styles.ctaRowCenter}>
            <Link href="#" className={styles.ctaPrimary}>See full plans</Link>
          </div>
        </div>
      </section>

      {/* Feature Highlights */}
      <section className={styles.sectionAlt} id="highlights">
        <div className={styles.container}>
          <h2 className={styles.sectionTitle}>Highlights</h2>
          <div className={styles.grid4}>
            <MiniFeature label="99.9% uptime" />
            <MiniFeature label="SSD NVMe storage" />
            <MiniFeature label="24/7 support" />
            <MiniFeature label="Full root access" />
          </div>
        </div>
      </section>

      {/* Testimonials / Trust */}
      <section className={styles.section} id="trust">
        <div className={styles.container}>
          <h2 className={styles.sectionTitle}>Trusted by builders</h2>
          <div className={styles.testimonials}>
            <blockquote className={styles.quote}>
              “Latency dropped by 40% after moving to Stralix. Deployment literally took minutes.”
              <footer>— Alex R., Indie Dev</footer>
            </blockquote>
            <blockquote className={styles.quote}>
              “Rock‑solid uptime and responsive support. Exactly what our community servers needed.”
              <footer>— Mira K., Guild Admin</footer>
            </blockquote>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className={styles.finalCta} id="get-started">
        <div className={styles.container}>
          <h2>Get your server online in under 60 seconds</h2>
          <div className={styles.ctaRowCenter}>
            <Link href="#" className={styles.ctaPrimary}>Get Started</Link>
            <Link href="#" className={styles.ctaSecondary}>Talk to sales</Link>
          </div>
        </div>
      </section>
    </div>
  )
}

function OfferingCard({ title, desc }: { title: string; desc: string }) {
  return (
    <div className={styles.cardFeature}>
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

function MiniFeature({ label }: { label: string }) {
  return (
    <div className={styles.miniFeature}>{label}</div>
  )
}
