import './globals.css'
import type { Metadata } from 'next'
import Header from '@/components/Header'
import Footer from '@/components/Footer'

export const metadata: Metadata = {
  title: 'Stralix • Cloud Hosting for Builders',
  description: 'Premium web hosting, VPS, game servers, domains, and SSL — fast, secure, and scalable.',
  themeColor: '#0ea5e9',
  icons: { icon: '/icons/favicon.ico' },
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
