import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { IonicModule } from '@ionic/angular';
import { DrinkFormComponent } from './drink-form/drink-form.component';
import { DrinkGraphicComponent } from './drink-graphic/drink-graphic.component';
import { DrinkMenuPage } from './drink-menu.page';

const routes: Routes = [
  {
    path: '',
    component: DrinkMenuPage,
  },
];

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    RouterModule.forChild(routes),
  ],
  entryComponents: [DrinkFormComponent],
  declarations: [DrinkMenuPage, DrinkGraphicComponent, DrinkFormComponent],
})
export class DrinkMenuPageModule {}
