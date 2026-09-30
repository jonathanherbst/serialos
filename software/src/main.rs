#[derive(serde::Serialize, serde::Deserialize)]
struct Config {
    volumes: Vec<Volume>,
}

#[derive(serde::Serialize, serde::Deserialize)]
struct Volume {
    device: String,
}

fn main() {
    //std::process::Command::new("btrfs").arg()
    println!("Hello, world changed!");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_volume() {
        let config: Config = yaml_serde::from_str("
            volumes:
                - device: mydevice
        ").expect("failed to parse configuration");

        assert_eq!(config.volumes.len(), 1);
        assert_eq!(config.volumes[0].device, "mydevice");
    }
}
