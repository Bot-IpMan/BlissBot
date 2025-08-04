// Configuration for the Appium server itself. This does **not** set the
// address of the Android emulator; instead it defines how clients reach the
// Appium service. The emulator/device must be connected separately via ADB
// (default port 5555).
module.exports = {
  server: {
    // Default Appium HTTP port. ADB connections use a different port (5555).
    port: 4723,
    // Listen on all network interfaces so containers or remote clients can
    // reach the server regardless of their IP.
    address: '0.0.0.0',
    // Log verbosity for easier debugging.
    logLevel: 'info'
  }
};
