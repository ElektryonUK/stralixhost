import styles from './page.module.css'

export default function HomePage() {
  return (
    <main className={styles.main}>
      <div className={styles.container}>
        <header className={styles.header}>
          <h1 className={styles.title}>Welcome to Stralixhost</h1>
          <p className={styles.description}>
            A modern full-stack web application built with Next.js and TypeScript
          </p>
        </header>

        <div className={styles.grid}>
          <div className={styles.card}>
            <h2>Getting Started</h2>
            <p>
              This is the initial setup of your Stralixhost application.
              Start building your features here!
            </p>
          </div>

          <div className={styles.card}>
            <h2>Documentation</h2>
            <p>
              Learn more about the project structure and development workflow
              in our README file.
            </p>
          </div>

          <div className={styles.card}>
            <h2>Development</h2>
            <p>
              Run <code className={styles.code}>npm run dev</code> to start the
              development server and begin building your application.
            </p>
          </div>

          <div className={styles.card}>
            <h2>Deploy</h2>
            <p>
              Ready to deploy? Build your application with{' '}
              <code className={styles.code}>npm run build</code>
            </p>
          </div>
        </div>

        <footer className={styles.footer}>
          <p>&copy; 2025 Stralixhost. All rights reserved.</p>
        </footer>
      </div>
    </main>
  )
}
