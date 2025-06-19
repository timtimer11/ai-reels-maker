'use client'

import Link from 'next/link'
import { SignInButton, SignedIn, SignedOut, UserButton } from '@clerk/nextjs'

const navigationItems = [
  { name: 'Home', href: '/' },
  { name: 'Contact', href: '/contact' },
  { name: 'Launch App', href: '/generate-video' },
]

export function Navigation() {
  return (
    <nav className="bg-gray-900 text-white py-4">
      <div className="flex items-center justify-center gap-8">
        {navigationItems.map(({ name, href }) => (
          <Link 
            key={href} 
            href={href}
            className="hover:text-blue-400 transition-colors"
          >
            {name}
          </Link>
        ))}
        
        <SignedOut>
          <SignInButton mode="modal">
            <button className="hover:text-blue-400 transition-colors">
              Sign In
            </button>
          </SignInButton>
        </SignedOut>
        <SignedIn>
          <span className="hover:text-blue-400 transition-colors">
            <UserButton afterSignOutUrl="/" />
          </span>
        </SignedIn>
      </div>
    </nav>
  )
} 