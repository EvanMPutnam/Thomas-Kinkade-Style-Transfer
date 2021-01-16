//
//  main.swift
//  KinkadeCMD
//
//  Created by Evan Putnam on 1/15/21.
//
import Foundation
import Vision
import CreateML
import CoreML
import CoreImage

let args = CommandLine.arguments
if (!(args.count > 2)) {
    print("Error: Invalid number of arguments.  Please provide a path for image and path for image out.")
    print(args)
    exit(EXIT_FAILURE)
}

let pathOfImage = args[1]
let pathOfOutImage = args[2]

print(args)

let model = try! Kinkade(configuration: MLModelConfiguration())
let input = try! KinkadeInput(imageAt: URL(fileURLWithPath: pathOfImage))
let out = try! model.prediction(input: input)
let outCIImage = CIImage(cvImageBuffer: out.stylizedImage)
let context = CIContext()
try! context.writePNGRepresentation(of: outCIImage,
                                    to: URL(fileURLWithPath: pathOfOutImage),
                                    format: .RGBA16,
                                    colorSpace: CGColorSpace(name: CGColorSpace.sRGB)!,
                                    options: [:])
print("Finished Writing File.")
