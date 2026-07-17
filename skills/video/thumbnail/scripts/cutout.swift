// Subject cutout via Apple Vision (same engine as Photos' "lift subject").
// Usage: swift cutout.swift <input image> <output png>
import Foundation
import Vision
import CoreImage
import AppKit

guard CommandLine.arguments.count == 3 else {
    fputs("usage: swift cutout.swift <in> <out.png>\n", stderr)
    exit(1)
}
let inURL = URL(fileURLWithPath: CommandLine.arguments[1])
let outURL = URL(fileURLWithPath: CommandLine.arguments[2])

guard let ciImage = CIImage(contentsOf: inURL) else {
    fputs("cannot read \(inURL.path)\n", stderr)
    exit(1)
}

let request = VNGenerateForegroundInstanceMaskRequest()
let handler = VNImageRequestHandler(ciImage: ciImage)
try handler.perform([request])

guard let result = request.results?.first else {
    fputs("no foreground subject found\n", stderr)
    exit(1)
}

let maskedBuffer = try result.generateMaskedImage(
    ofInstances: result.allInstances,
    from: handler,
    croppedToInstancesExtent: true)

let masked = CIImage(cvPixelBuffer: maskedBuffer)
let context = CIContext()
guard let cgImage = context.createCGImage(masked, from: masked.extent) else {
    fputs("render failed\n", stderr)
    exit(1)
}

let rep = NSBitmapImageRep(cgImage: cgImage)
guard let png = rep.representation(using: .png, properties: [:]) else {
    fputs("png encode failed\n", stderr)
    exit(1)
}
try png.write(to: outURL)
print("wrote \(outURL.path) (\(cgImage.width)x\(cgImage.height))")
