export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header style={{padding:'12px 20px', borderBottom:'1px solid #eee', display:'flex', justifyContent:'space-between'}}>
          <div style={{fontWeight:600}}>Stralix Cloud</div>
          <nav style={{display:'flex', gap:16}}>
            <a href="/">Home</a>
            <a href="/pricing">Pricing</a>
            <a href="/features">Features</a>
            <a href="/panel">Panel</a>
            <a href="/auth/login">Login</a>
            <a href="/auth/register">Register</a>
          </nav>
        </header>
        <main>{children}</main>
        <footer style={{padding:'24px 20px', borderTop:'1px solid #eee', marginTop:40}}>
          <small>© {new Date().getFullYear()} Stralix Cloud · <a href="/legal/terms">Terms</a> · <a href="/legal/privacy">Privacy</a></small>
        </footer>
      </body>
    </html>
  );
}
