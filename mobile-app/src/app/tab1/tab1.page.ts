import { Component } from '@angular/core';
import { PhotoService } from '../services/photo.service';
import { Animation, AnimationController } from '@ionic/angular';

@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  styleUrls: ['tab1.page.scss']
})

export class Tab1Page {

  constructor(private animationCtrl: AnimationController,
    public photoService: PhotoService) {
  }

  addPhotoToGallery() {
    this.photoService.addNewToGallery();
  }
  // eslint-disable-next-line @angular-eslint/use-lifecycle-interface
  async ngOnInit() {
    console.log('Loading Images');
    await this.photoService.loadSaved();
  }
  selectImage(photo) {
    this.animationCtrl.create()
      .duration(2000)
      .iterations(2)
      .addAnimation(this.animationCtrl.create()
        .addElement(photo)
        .duration(5000)
        .keyframes([
          { offset: 0, transform: 'scale(1))', opacity: '0.5' },
          { offset: 0.5, transform: 'scale(0.8)', opacity: '1' },
          { offset: 1, transform: 'scale(1)', opacity: '0.5' }
        ]));
    console.log(photo);
  }
}
