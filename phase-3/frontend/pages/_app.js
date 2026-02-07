import '../styles/globals.css';
import FloatingChatWidget from '../components/FloatingChatWidget';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

function MyApp({ Component, pageProps }) {
  const router = useRouter();
  const [showChatWidget, setShowChatWidget] = useState(false);

  useEffect(() => {
    // Show chat widget only on dashboard page
    setShowChatWidget(router.pathname === '/dashboard');
  }, [router.pathname]);

  return (
    <>
      <Component {...pageProps} />
      {showChatWidget && <FloatingChatWidget />}
    </>
  );
}

export default MyApp;