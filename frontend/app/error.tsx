'use client'

import { useEffect } from 'react'
import styles from './error.module.css'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error('Application error:', error)
  }, [error])

  return (
    <div className={styles.container}>
      <div className={styles.content}>
        <h1 className={styles.title}>Something went wrong!</h1>
        <p className={styles.description}>
          We apologize for the inconvenience. An unexpected error occurred.
        </p>
        {process.env.NODE_ENV === 'development' && (
          <details className={styles.details}>
            <summary>Error details (development only)</summary>
            <pre className={styles.error}>{error.message}</pre>
          </details>
        )}
        <button
          className={styles.button}
          onClick={() => reset()}
        >
          Try again
        </button>
      </div>
    </div>
  )
}