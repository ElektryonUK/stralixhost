import { AuthProvider } from "@/components/auth/AuthProvider";
import { HeaderNav } from "@/components/layout/HeaderNav";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <HeaderNav />
          <main>{children}</main>
          <footer style={{padding:'24px 20px', borderTop:'1px solid #eee', marginTop:40}}>
            <small>© {new Date().getFullYear()} Stralix Cloud · <a href="/legal/terms">Terms</a> · <a href="/legal/privacy">Privacy</a></small>
          </footer>
        </AuthProvider>
      </body>
    </html>
  );
}
