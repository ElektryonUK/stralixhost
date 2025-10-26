import { AuthProvider } from "@/components/auth/AuthProvider";
import { HeaderNav } from "@/components/layout/HeaderNav";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ backgroundColor: "#0b1220", color: "#e2e8f0" }}>
        <AuthProvider>
          <HeaderNav />
          <main>{children}</main>
          <footer
            style={{
              padding: "24px 20px",
              borderTop: "1px solid rgba(148,163,184,0.2)",
              marginTop: 40,
              color: "#94a3b8",
            }}
          >
            <small>
              © {new Date().getFullYear()} Stralix Cloud ·{" "}
              <a href="/legal/terms" style={{ color: "#cbd5e1" }}>
                Terms
              </a>{" "}
              ·{" "}
              <a href="/legal/privacy" style={{ color: "#cbd5e1" }}>
                Privacy
              </a>
            </small>
          </footer>
        </AuthProvider>
      </body>
    </html>
  );
}
