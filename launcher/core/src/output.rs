use serde::{
    Serialize,
    Serializer,
};
use serde_json::{
    json,
    Value,
};


#[derive(Debug, Clone, Copy)]
pub enum Status {
    Success,
    Failure,
}


impl Serialize for Status {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        match self {
            Status::Success =>
                serializer.serialize_bool(true),
            Status::Failure =>
                serializer.serialize_bool(false),
        }
    }
}


#[derive(Serialize)]
pub struct Response {
    pub status: Status,
    pub data: Value,
    pub message: String,
}


impl Response {
    pub fn success(data: Value, message: &str) -> Self {
        Self {
            status: Status::Success,
            data,
            message: message.to_string(),
        }
    }

    pub fn failure(data: Value, message: &str) -> Self {
        Self {
            status: Status::Failure,
            data,
            message: message.to_string(),
        }
    }

    pub fn ok(message: &str) -> Self {
        Self::success(json!({}), message)
    }

    pub fn err(message: &str) -> Self {
        Self::failure(json!({}), message)
    }

    pub fn send(&self) {
        if let Ok(json_string) = serde_json::to_string(self) {
            println!("{}", json_string);
        }
    }
}