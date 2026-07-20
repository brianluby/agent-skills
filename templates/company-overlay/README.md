# Company overlay template

Copy this directory into a **new private Git repository**. Do not develop company-only skills in the public marketplace and do not push this template back with internal content.

Before using it:

1. Replace `YOUR_COMPANY` and `YOUR_ORG` in `apm.yml` and package metadata.
2. Rename `company-context` to a company-specific capability.
3. Replace the placeholder skill with internal, reviewed guidance.
4. Make the repository private and restrict access through your Git provider.
5. Add the private marketplace alongside public packages in each company repository's `apm.yml`.

The private package can use public packages such as `foundation` and `rust`, but this public repository must never consume packages from the private overlay.
