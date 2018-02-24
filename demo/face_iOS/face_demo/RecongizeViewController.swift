//
//  RecongizeViewController.swift
//  face_demo
//
//  Created by zhangsl on 2018/1/25.
//  Copyright © 2018年 zytec. All rights reserved.
//

import UIKit
import AFNetworking
import MBProgressHUD


class RecongizeViewController: UIViewController {
    
    lazy var imageView: UIImageView = {
        let imageView = UIImageView()
        imageView.contentMode = .scaleAspectFill
        imageView.clipsToBounds = true
        imageView.layer.borderWidth = 1
        imageView.layer.borderColor = UIColor.orange.cgColor
        
        return imageView
    }()
    
    lazy var recognizeButton: UIButton = {
        let button = UIButton(type: .custom)
        button.setTitle("人脸识别", for: .normal)
        button.titleLabel?.font = UIFont.systemFont(ofSize: 18)
        button.setTitleColor(UIColor.white, for: .normal)
        button.backgroundColor = UIColor.orange
        button.addTarget(self, action:#selector(recognizeAction), for: .touchUpInside)
        
        return button;
    }()
    
    lazy var label: UILabel = {
        let label = UILabel()
        label.font = UIFont.systemFont(ofSize: 20)
        label.textColor = UIColor.gray;
        label.textAlignment = .center
        
        return label
    }()

    override func viewDidLoad() {
        super.viewDidLoad()
        
        title = "人脸识别"
        view.backgroundColor = UIColor.white

        view.addSubview(imageView)
        view.addSubview(recognizeButton)
        view.addSubview(label)
    }
    
    override func viewDidLayoutSubviews() {
         super.viewDidLayoutSubviews()
        
        let imageX: CGFloat = 0;
        let imageY: CGFloat = 64;
        let imageW: CGFloat = view.frame.width
        let imageH: CGFloat = imageW
        imageView.frame = CGRect(x: imageX, y: imageY, width: imageW, height: imageH)
        
        let buttonX: CGFloat = 0
        let buttonH: CGFloat = 44
        let buttonW = imageW
        let buttonY: CGFloat = view.frame.height - buttonH
        recognizeButton.frame = CGRect(x: buttonX, y: buttonY, width: buttonW, height: buttonH)
    
        let labelX: CGFloat = 0
        let labelY: CGFloat = imageView.frame.maxY
        let labelW: CGFloat = imageView.frame.width
        let labelH: CGFloat = view.frame.height - imageH - 64 - buttonH
        label.frame = CGRect(x: labelX, y: labelY, width: labelW, height: labelH)
    }
}


extension RecongizeViewController: UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    
    @objc
    func recognizeAction() {
        let imagePicker = UIImagePickerController()
        imagePicker.sourceType = .camera
        imagePicker.allowsEditing = true;
        imagePicker.delegate = self
        present(imagePicker, animated: true, completion: nil)
    }
    
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : Any]) {
        dismiss(animated: true, completion: nil)
        let image = info["UIImagePickerControllerEditedImage"] as! UIImage
        imageView.image = image
        uploadImage(image: image)
    }
}


extension RecongizeViewController {
    
    func uploadImage(image: UIImage) {
        let hud = MBProgressHUD.showAdded(to: view, animated: true)
        hud.label.text = "正在识别..."
        
        let manager = AFHTTPSessionManager()
        manager.responseSerializer.acceptableContentTypes = Set(["text/json", "application/json"])
        
        manager.post("\(server)/recognize_face", parameters: nil, constructingBodyWith: { (formData) in
            let data = UIImageJPEGRepresentation(image, 0.6)
            formData.appendPart(withFileData: data!, name: "file", fileName: "file", mimeType: "image/jpeg")
        }, progress: nil, success: { (task, result) in
            hud.hide(animated: true)
            self.label.text = (result as! [String: Any])["message"] as? String
        }) { (task, error) in
            hud.hide(animated: true)
            self.label.text = "Error"
        }
    }
}
