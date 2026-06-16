export interface ModelProvider {
  name: string
  description: string
  base_url: string | null
  models: ModelOption[]
  requires_base_url: boolean
}

export interface ModelOption {
  id: string
  name: string
  description: string
}

export interface ModelConfig {
  provider: string
  model_name: string
  api_key: string
  base_url?: string
  temperature: number
  max_tokens: number
}

export interface ModelConfigResponse {
  provider: string
  model_name: string
  base_url: string | null
  temperature: number
  max_tokens: number
  is_configured: boolean
}

export interface TestConnectionResult {
  success: boolean
  message: string
  latency_ms?: number
}
