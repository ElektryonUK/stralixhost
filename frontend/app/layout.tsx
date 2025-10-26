import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Stralixhost',
  description: 'Full-stack web application built with modern technologies',
  keywords: ['web app', 'full-stack', 'next.js', 'react'],
  authors: [{ name: 'Stralixhost Team' }],
  viewport: 'width=device-width, initial-scale=1',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <div id="root">
          {children}
        </div>
      </body>
    </html>
  )
}