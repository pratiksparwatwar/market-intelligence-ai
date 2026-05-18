"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { TrendingUp, LayoutDashboard, Layers, BarChart2, Newspaper, Settings } from "lucide-react";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/themes", label: "Themes", icon: Layers },
  { href: "/assets", label: "Assets", icon: BarChart2 },
  { href: "/sources", label: "Sources", icon: Newspaper },
  { href: "/admin", label: "Admin", icon: Settings },
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav className="bg-gray-900 border-b border-gray-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/dashboard" className="flex items-center gap-2 text-white font-bold text-lg">
            <TrendingUp className="h-6 w-6 text-blue-400" />
            <span className="hidden sm:block">Market Intelligence AI</span>
            <span className="sm:hidden">MI AI</span>
          </Link>
          <div className="flex items-center gap-1">
            {navItems.map(({ href, label, icon: Icon }) => {
              const active = pathname === href || pathname.startsWith(href + "/");
              return (
                <Link
                  key={href}
                  href={href}
                  className={`flex items-center gap-1.5 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    active
                      ? "bg-blue-600 text-white"
                      : "text-gray-400 hover:text-white hover:bg-gray-800"
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span className="hidden md:block">{label}</span>
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </nav>
  );
}
