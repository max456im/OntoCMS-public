```rust
// SPDX-License-Identifier: GPL-3.0-only
// OntoCoder — LSP Server for Editors (VS Code, Vim, etc.)

use async_trait::async_trait;
use lsp_server::{Connection, Message, Request, Response};
use lsp_types::*;
use serde_json::Value;

use crate::ontocoder::validator::{OntoValidator, ValidationError};
use crate::ontocoder::license_registry::LicenseRegistry;
use crate::core::activity_ledger::ProfileId;

pub struct OntoLspServer {
    validator: OntoValidator,
    capabilities: ServerCapabilities,
}

impl OntoLspServer {
    pub fn new(profiles: Vec<ProfileId>) -> Self {
        let registry = LicenseRegistry::new();
        let validator = OntoValidator::new(registry, profiles);
        Self {
            validator,
            capabilities: ServerCapabilities {
                text_document_sync: Some(TextDocumentSyncCapability::Kind(
                    TextDocumentSyncKind::FULL,
                )),
                hover_provider: Some(HoverProviderCapability::Simple(true)),
                diagnostics_provider: Some(DiagnosticsCapability::Simple(true)),
                ..Default::default()
            },
        }
    }

    pub async fn run(&self) -> anyhow::Result<()> {
        let (connection, io_threads) = Connection::stdio();
        let server_capabilities = serde_json::to_value(&self.capabilities).unwrap();
        let initialization_params = connection.initialize(server_capabilities)?;
        self.main_loop(&connection, initialization_params)?;
        io_threads.join()?;
        Ok(())
    }

    fn main_loop(&self, connection: &Connection, _: serde_json::Value) -> anyhow::Result<()> {
        loop {
            match connection.receiver.recv()? {
                Message::Request(req) => {
                    if connection.handle_shutdown(&req)? {
                        return Ok(());
                    }
                    self.on_request(connection, req)?;
                }
                Message::Notification(_) => {
                    // Игнорируем нотификации (например, didOpen, didChange — обрабатываем через didSave)
                }
                Message::Response(_) => {}
            }
        }
    }

    fn on_request(&self, connection: &Connection, req: Request) -> anyhow::Result<()> {
        match req.method.as_str() {
            "textDocument/hover" => {
                // Показываем онтологический профиль при наведении
                let _params: HoverParams = serde_json::from_value(req.params)?;
                let result = Hover {
                    contents: HoverContents::Scalar(MarkedString::String(
                        "OntoCMS: Hover over ONTO-PROFILE to see perceptual/behavioral traits".into(),
                    )),
                    range: None,
                };
                let resp = Response::new_ok(req.id, result);
                connection.sender.send(Message::Response(resp))?;
            }
            _ => {
                // Diagnostics генерируются при сохранении (внешний hook)
            }
        }
        Ok(())
    }

    /// Публичный метод для CLI и CI: генерация diagnostics
    pub fn diagnostics_for_file(&self, uri: &str, content: &str) -> Vec<Diagnostic> {
        let mut diagnostics = vec![];
        match self.validator.validate_file(&std::path::Path::new(uri), content) {
            Err(ValidationError::EnergyValueDetected) => {
                diagnostics.push(Diagnostic::new_simple(
                    Range::new(Position::new(0, 0), Position::new(0, 10)),
                    "Energy/value metric detected — forbidden by SGRL-α".into(),
                ));
            }
            Err(ValidationError::LicenseIncompatible(lic)) => {
                diagnostics.push(Diagnostic::new_simple(
                    Range::new(Position::new(0, 0), Position::new(0, 10)),
                    format!("License {} incompatible with SGCL", lic),
                ));
            }
            Err(ValidationError::ProfileNotInRegistry(_)) => {
                diagnostics.push(Diagnostic::new_simple(
                    Range::new(Position::new(0, 0), Position::new(0, 10)),
                    "Invalid or missing ONTO-PROFILE".into(),
                ));
            }
            Err(ValidationError::PhaseAnnotationMissing) => {
                diagnostics.push(Diagnostic::new_simple(
                    Range::new(Position::new(0, 0), Position::new(0, 10)),
                    "Missing ONTO-PHASE annotation".into(),
                ));
            }
            Err(ValidationError::AENGAViolation) => {
                diagnostics.push(Diagnostic::new_simple(
                    Range::new(Position::new(0, 0), Position::new(0, 10)),
                    "AENGA violation: remote control or ethics override detected".into(),
                ));
            }
            Ok(()) => {}
        }
        diagnostics
    }
}
```