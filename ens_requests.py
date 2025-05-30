export const BENS_API_RESOURCES = {
  addresses_lookup: {
    path: '/api/v1/:chainId/addresses\\:lookup',
    pathParams: [ 'chainId' as const ],
    filterFields: [ 'address' as const, 'resolved_to' as const, 'owned_by' as const, 'only_active' as const, 'protocols' as const ],
    paginated: true,
  },
  address_domain: {
    path: '/api/v1/:chainId/addresses/:address',
    pathParams: [ 'chainId' as const, 'address' as const ],
  },
  domain_info: {
    path: '/api/v1/:chainId/domains/:name',
    pathParams: [ 'chainId' as const, 'name' as const ],
  },
  domain_events: {
    path: '/api/v1/:chainId/domains/:name/events',
    pathParams: [ 'chainId' as const, 'name' as const ],
  },
  domains_lookup: {
    path: '/api/v1/:chainId/domains\\:lookup',
    pathParams: [ 'chainId' as const ],
    filterFields: [ 'name' as const, 'only_active' as const, 'protocols' as const ],
    paginated: true,
  },
  domain_protocols: {
    path: '/api/v1/:chainId/protocols',
    pathParams: [ 'chainId' as const ],
  },
} satisfies Record<string, ApiResource>;

