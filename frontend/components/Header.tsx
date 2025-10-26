import Link from 'next/link'
import styles from './Header.module.css'

export default function Header() {
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <Link href="/" className={styles.brand}>
          <span className={styles.logoDot} />
          <span className={styles.brandText}>Stralix</span>
        </Link>
        <nav className={styles.nav} aria-label="Main Navigation">
          {/* Placeholder for future nav items */}
          <div className={styles.navPlaceholder} />
        </nav>
        <div className={styles.actions}>
          <Link href="#" className={styles.actionGhost}>Docs</Link>
          <Link href="#" className={styles.actionPrimary}>Get Started</Link>
        </div>
      </div>
    </header>
  )
}
