//
//  ViewController.swift
//  face_demo
//
//  Created by zhangsl on 2018/1/25.
//  Copyright © 2018年 zytec. All rights reserved.
//

import UIKit


class ViewController: UIViewController {
    
    lazy var recognizeButton: UIButton = {
        let button = UIButton(type: .custom)
        button.setTitle("识别人脸", for: .normal)
        button.titleLabel?.font = UIFont.systemFont(ofSize: 18)
        button.setTitleColor(UIColor.white, for: .normal)
        button.backgroundColor = UIColor.orange
        button.addTarget(self, action:#selector(recognizeAction), for: .touchUpInside)
        
        return button;
    }()

    lazy var takeButton: UIButton = {
        let button = UIButton(type: .custom)
        button.setTitle("采集人脸", for: .normal)
        button.titleLabel?.font = UIFont.systemFont(ofSize: 18)
        button.setTitleColor(UIColor.white, for: .normal)
        button.backgroundColor = UIColor.orange
        button.addTarget(self, action:#selector(takeAction), for: .touchUpInside)
        
        return button;
    }()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        view.backgroundColor = UIColor.white
        view.addSubview(self.recognizeButton)
        view.addSubview(self.takeButton)
    }
    
    override func viewDidLayoutSubviews() {
        super.viewDidLayoutSubviews()
        
        let rX: CGFloat = 20
        let rY: CGFloat = 150
        let rW: CGFloat = view.frame.size.width - 2 * rX
        let rH: CGFloat = 44
        self.recognizeButton.frame = CGRect(x: rX, y: rY, width: rW, height: rH)
        
        let tX: CGFloat = rX;
        let tY: CGFloat = rY + 100
        let tW = rW
        let tH = rH
        self.takeButton.frame = CGRect(x: tX, y: tY, width: tW, height: tH)
    }

    @objc
    func recognizeAction() {
        let vc = RecongizeViewController()
        navigationController?.pushViewController(vc, animated: true)
    }
    
    @objc
    func takeAction() {
        let vc = TakeViewController()
        navigationController?.pushViewController(vc, animated: true)
    }
}

