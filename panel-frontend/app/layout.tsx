import "./globals.css";
import { AuthProvider } from "../components/auth/AuthProvider";
import { HeaderNav } from "../components/layout/HeaderNav";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <HeaderNav />
          <main>{children}</main>
          <footer className="container" style={{borderTop:"1px solid rgba(148,163,184,0.2)", marginTop:40, color: "#94a3b8"}}>
            <small>© {new Date().getFullYear()} Stralix Cloud · <a href="/legal/terms" className="text-dim">Terms</a> · <a href="/legal/privacy" className="text-dim">Privacy</a></small>
          </footer>
        </AuthProvider>
      </body>
    </html>
  );
}
