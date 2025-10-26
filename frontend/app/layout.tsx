import './globals.css'
import type { Metadata, Viewport } from 'next'
import Header from '@/components/Header'
import Footer from '@/components/Footer'

export const metadata: Metadata = {
  title: 'Stralix • Premium Hosting for Builders',
  description: 'Web hosting, VPS, game servers, domains, and SSL — fast, secure, and scalable.',
  icons: { icon: '/icons/favicon.ico' },
}

export const viewport: Viewport = {
  themeColor: '#0ea5e9',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <Header />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  )
}
