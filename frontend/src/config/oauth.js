export const oidcConfig = {
  // URLs
  authority: 'https://auth.bigoscloud.com/application/o/smogwatch/',
  redirect_uri: window.location.origin + '/auth/callback',
  post_logout_redirect_uri: window.location.origin + '/',

  // Client - You'll need to configure this in Authentik for SmogWatch
  client_id: 'ToADLuYgQkxnujamNvH0QqMBbLWkt50GIpoXeLJ5', // Replace with actual client ID from Authentik

  // Scopes and response
  scope: 'openid profile email offline_access', // openid should be first
  response_type: 'code', // Explicit for public client

  // Token/user info
  loadUserInfo: true,

  // Session/renewal
  automaticSilentRenew: true, // Enable automatic token refresh
  monitorSession: true,
  checkSessionIntervalInSeconds: 2,

  // For public clients, PKCE is handled automatically by oidc-client-ts
}
