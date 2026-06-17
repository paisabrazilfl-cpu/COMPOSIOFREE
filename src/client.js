export class ComposioClient {
  constructor() {
    this.integrations = new Map();
  }

  registerIntegration(name, config) {
    this.integrations.set(name, config);
    return { status: 'registered', integration: name };
  }

  getIntegration(name) {
    const integration = this.integrations.get(name);
    if (!integration) {
      throw new Error(`Integration ${name} not found`);
    }
    return integration;
  }
}
