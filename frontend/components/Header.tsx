import Link from 'next/link'
import styles from './Header.module.css'
import { Suspense } from 'react'

function AuthActions() {
  // Placeholder for dynamic auth-aware header; replace with real hook that calls /api/me
  // This keeps UI ready; real implementation will hydrate state from backend
  const isAuthenticated = false
  if (!isAuthenticated) {
    return (
      <div className={styles.actions}>
        <Link href="/login" className={styles.actionGhost}>Login</Link>
        <Link href="/register" className={styles.actionPrimary}>Register</Link>
      </div>
    )
  }
  return (
    <div className={styles.userMenu}>
      <div className={styles.avatar} aria-label="Account menu">S</div>
      <div className={styles.dropdown}>
        <Link href="/account">Account</Link>
        <Link href="/billing">Billing</Link>
        <form action="/api/logout" method="post"><button type="submit">Logout</button></form>
      </div>
    </div>
  )
}

export default function Header() {
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <Link href="/" className={styles.brand}>
          <span className={styles.logoDot} />
          <span className={styles.brandText}>Stralix</span>
        </Link>
        <nav className={styles.nav} aria-label="Main Navigation">
          <div className={styles.navPlaceholder} />
        </nav>
        <Suspense fallback={<div className={styles.actions} />}> 
          <AuthActions />
        </Suspense>
      </div>
    </header>
  )
}
