package com.productionlogger.data

import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * 모델 정보 데이터 클래스
 * 생산 모델의 기본 정보를 저장합니다.
 */
@Entity(tableName = "model_info")
data class ModelInfo(
    @PrimaryKey
    val modelName: String,      // 모델명 (기본키)
    val unitPrice: Int,         // 단가
    val description: String     // 설명
)
