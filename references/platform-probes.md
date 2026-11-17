# Platform-specific probes

Use only the relevant section. These are prompts for evidence collection, not a requirement to run every check.

## Web application

- Start from a clean dependency install and production build.
- Verify the production entry point, not only hot-reload development mode.
- Exercise one complete journey with a fresh browser profile.
- Check refresh, direct navigation, expired session, slow/failed request, and persistence where relevant.
- Distinguish browser-local storage from server persistence.
- Record console errors and failed network requests during core journeys.
- If a deployment is promised, verify the deployed URL and its version identity.

## Android

- Record application ID, version name/code, ABI support, minimum/target SDK, signature state, and APK/AAB hash.
- Install on a clean emulator or authorized device; do not treat successful compilation as successful installation.
- Test first launch, permission denial, background/foreground transition, restart, and upgrade from the prior supported version where applicable.
- Identify whether network-backed features still work outside the developer machine.
- Make clear whether the deliverable is an installable APK or a Play Store bundle.

## iOS/macOS

- Record bundle ID, version/build, target OS, architecture, signing/notarization state, and artifact hash.
- Separate simulator success from device-install success.
- Verify first launch, permission denial, relaunch, persistence, and upgrade where relevant.
- Do not claim distributability when signing, provisioning, or notarization is absent.

## Windows/Linux desktop

- Distinguish portable binaries from installers.
- Verify architecture, runtime dependencies, user-data location, first launch, relaunch, uninstall, and upgrade behavior.
- Test outside the source tree so undeclared local files do not mask packaging errors.
- Record code-signing state when the release claims trust or enterprise distribution.

## CLI or library

- Install into a fresh environment using the documented public method.
- Verify `--help`, version output, one successful operation, one failure, exit codes, stdout/stderr boundaries, and clean uninstall where applicable.
- For a library, test the documented import and minimal public API from a separate consumer project.
- Do not treat private test imports as proof that packaging works.

## Backend or API

- Verify startup from declared configuration, health/readiness behavior, schema or migration application, authentication boundaries, and one complete write/read journey.
- Restart the service and verify committed data persists.
- Exercise invalid input and unavailable dependency behavior.
- Never use production data or destructive endpoints without explicit authorization.
