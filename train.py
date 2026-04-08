from ultralytics import YOLO

def main():
    model = YOLO("yolo26n.pt")
    results = model.train(
        data="data.yaml",
        epochs=50,
        optimizer="MuSGD",
        fraction=1.0,
        cache=True
    )

if __name__ == "__main__":
    main()
