//
//  TakeViewController.swift
//  face_demo
//
//  Created by zhangsl on 2018/1/25.
//  Copyright © 2018年 zytec. All rights reserved.
//

import UIKit
import AFNetworking
import MBProgressHUD


class TakeViewController: UIViewController {

    lazy var imageView: UIImageView = {
        let imageView = UIImageView()
        imageView.contentMode = .scaleAspectFill
        imageView.clipsToBounds = true
        imageView.layer.borderWidth = 1
        imageView.layer.borderColor = UIColor.orange.cgColor
        
        return imageView
    }()
    
    lazy var takeButton: UIButton = {
        let button = UIButton(type: .custom)
        button.setTitle("人脸采集", for: .normal)
        button.titleLabel?.font = UIFont.systemFont(ofSize: 18)
        button.setTitleColor(UIColor.white, for: .normal)
        button.backgroundColor = UIColor.orange
        button.addTarget(self, action:#selector(takeAction), for: .touchUpInside)
        
        return button;
    }()
    
    lazy var textFiled: UITextField = {
        let textFiled = UITextField()
        textFiled.font = UIFont.systemFont(ofSize: 20)
        textFiled.textAlignment = .center
        textFiled.layer.borderColor = UIColor.orange.cgColor;
        textFiled.layer.borderWidth = 1
        textFiled.placeholder = "请输入人脸姓名"
        
        return textFiled
    }()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        title = "人脸采集"
        view.backgroundColor = UIColor.white
        
        view.addSubview(imageView)
        view.addSubview(takeButton)
        view.addSubview(textFiled)
        textFiled.delegate = self
    }
    
    override func viewDidLayoutSubviews() {
        super.viewDidLayoutSubviews()
        
        let textFiledX: CGFloat = 0
        let textFiledY: CGFloat = 64
        let textFiledW: CGFloat = view.frame.width
        let textFiledH: CGFloat = 44
        textFiled.frame = CGRect(x: textFiledX, y: textFiledY, width: textFiledW, height: textFiledH)
        
        let imageX: CGFloat = 0;
        let imageY: CGFloat = textFiled.frame.maxY + 10;
        let imageW: CGFloat = view.frame.width
        let imageH: CGFloat = imageW
        imageView.frame = CGRect(x: imageX, y: imageY, width: imageW, height: imageH)
        
        let buttonX: CGFloat = 0
        let buttonH: CGFloat = 44
        let buttonW = imageW
        let buttonY: CGFloat = view.frame.height - buttonH
        takeButton.frame = CGRect(x: buttonX, y: buttonY, width: buttonW, height: buttonH)
    }
    
    override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent?) {
        view.endEditing(true)
    }
}


extension TakeViewController: UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    
    @objc
    func takeAction() {
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


extension TakeViewController {
    
    func uploadImage(image: UIImage) {
        let hud = MBProgressHUD.showAdded(to: view, animated: true)
        hud.label.text = "正在上传..."
        
        let manager = AFHTTPSessionManager()
        manager.responseSerializer.acceptableContentTypes = Set(["text/json", "application/json"])
        
        let params = ["name": textFiled.text]
        
        manager.post("\(server)/upload_face", parameters: params, constructingBodyWith: { (formData) in
            let data = UIImageJPEGRepresentation(image, 0.6)
            formData.appendPart(withFileData: data!, name: "file", fileName: "file", mimeType: "image/jpeg")
        }, progress: nil, success: { (task, result) in
            hud.hide(animated: true)
            
            let hud = MBProgressHUD.showAdded(to: self.view, animated: true)
            hud.label.text = "人脸采集成功"
            hud.mode = .text
            hud.hide(animated: true, afterDelay: 2)
        }) { (task, error) in
            hud.hide(animated: true)
            
            let hud = MBProgressHUD.showAdded(to: self.view, animated: true)
            hud.label.text = "未采集到人脸"
            hud.mode = .text
            hud.hide(animated: true, afterDelay: 2)
        }
    }
}


extension TakeViewController: UITextFieldDelegate {
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        view.endEditing(true)
        return true
    }
}
