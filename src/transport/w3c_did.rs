```rust
// SPDX-License-Identifier: GPL-3.0-only
// W3C Decentralized Identifier (DID) Integration — AENGA-Compliant

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct DidDocument {
    #[serde(rename = "@context")]
    pub context: String,
    pub id: String, // e.g., did:key:z6Mk...
    pub verification_method: Vec<VerificationMethod>,
    pub authentication: Vec<String>,
    pub service: Vec<ServiceEndpoint>,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct VerificationMethod {
    pub id: String,
    #[serde(rename = "type")]
    pub method_type: String, // e.g., "JsonWebKey2020"
    pub controller: String,
    #[serde(flatten)]
    pub key_data: HashMap<String, serde_json::Value>,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct ServiceEndpoint {
    pub id: String,
    #[serde(rename = "type")]
    pub service_type: String, // e.g., "OntoCMS/PublicHub"
    pub service_endpoint: String,
}

/// Генерация DID-документа для ontoCMS-узла
pub fn generate_did_document(
    profile_id: &str,
    public_key_pem: &str,
    public_hub_endpoint: &str,
) -> DidDocument {
    let did = format!("did:key:{}", blake3::hash(public_key_pem.as_bytes()).to_hex());

    DidDocument {
        context: "https://www.w3.org/ns/did/v1".to_string(),
        id: did.clone(),
        verification_method: vec![VerificationMethod {
            id: format!("{}#key-1", did),
            method_type: "JsonWebKey2020".to_string(),
            controller: did.clone(),
            key_data: [("publicKeyPem".to_string(), public_key_pem.into())]
                .into_iter()
                .collect(),
        }],
        authentication: vec![format!("{}#key-1", did)],
        service: vec![ServiceEndpoint {
            id: format!("{}#ontoCMS", did),
            service_type: "OntoCMS/PublicHub".to_string(),
            service_endpoint: public_hub_endpoint.to_string(),
        }],
    }
}

/// Проверка: DID не должен использоваться для внешнего управления
pub fn validate_did_usage(service_type: &str) -> Result<(), TransportError> {
    // AENGA: запрет на сервисы, подразумевающие контроль
    if service_type.contains("RemoteControl") || service_type.contains("Governance") {
        Err(TransportError::AENGAViolation)
    } else {
        Ok(())
    }
}

#[derive(Debug)]
pub enum TransportError {
    AENGAViolation,
    InvalidFormat,
}
```