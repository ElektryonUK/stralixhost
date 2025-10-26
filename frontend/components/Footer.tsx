import styles from './Footer.module.css'

export default function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.container}>
        <div className={styles.grid}>
          <div className={styles.brandBlock}>
            <div className={styles.logoRow}>
              <span className={styles.logoDot} />
              <span className={styles.brand}>Stralix</span>
            </div>
            <p className={styles.copy}>Premium cloud built for builders.</p>
          </div>
          <div className={styles.links}>
            <a href="#">Status</a>
            <a href="#">Security</a>
            <a href="#">Privacy</a>
            <a href="#">Terms</a>
          </div>
        </div>
        <div className={styles.line} />
        <div className={styles.legal}>© {new Date().getFullYear()} Stralixhost. All rights reserved.</div>
      </div>
    </footer>
  )
}
