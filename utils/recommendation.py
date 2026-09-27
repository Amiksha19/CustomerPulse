def get_recommendations(customer, probability, customer_stage):

    recommendations = []
    customer_stage = str(customer_stage).strip().lower()

    if customer_stage == "visitor":

        if probability >= 0.70:
            recommendations.append("🎁 Offer a first-time subscription discount")
            if customer["Customer_Satisfaction"] <= 4:
                recommendations.append("😊 Improve the customer experience before subscription")
            if customer["Daily_Watch_Time"] < 2:
                recommendations.append("🎬 Recommend personalized content")
            recommendations.append("⭐ Recommend a suitable subscription plan")

        elif probability >= 0.30:
            recommendations.append("🎬 Recommend personalized content")
            recommendations.append("🎁 Offer a first-time subscription incentive")
            recommendations.append("⭐ Recommend a suitable subscription plan")
            if customer["Daily_Watch_Time"] < 2:
                recommendations.append("📺 Recommend trending shows")

        else:
            recommendations.append("🎁 Provide a first-time subscriber offer")
            recommendations.append("🎬 Recommend personalized content")
            recommendations.append("🎉 Offer early access to selected new releases")

    elif customer_stage == "subscriber":

        if probability >= 0.70:
            recommendations.append("🎁 Give renewal retention discount")
            if customer["Customer_Satisfaction"] <= 4:
                recommendations.append("📞 Contact customer personally")
            if customer["Support_Queries"] >= 5:
                recommendations.append("🛠 Resolve customer complaints immediately")
            if customer["Days_Since_Last_Activity"] >= 30:
                recommendations.append("📧 Send 'We Miss You' email")
            if customer["Daily_Watch_Time"] < 2:
                recommendations.append("🎬 Recommend trending content")
            if customer["Subscription_Plan"] == "Basic":
                recommendations.append("⭐ Offer Premium Trial")
            elif customer["Subscription_Plan"] == "Standard":
                recommendations.append("💎 Offer Premium Upgrade")

        elif probability >= 0.30:
            recommendations.append("🎬 Recommend personalized content")
            recommendations.append("🎁 Give loyalty reward")
            if customer["Customer_Satisfaction"] <= 6:
                recommendations.append("😊 Improve customer experience")
            if customer["Subscription_Plan"] == "Basic":
                recommendations.append("⭐ Recommend Standard Plan")
            elif customer["Subscription_Plan"] == "Standard":
                recommendations.append("💎 Recommend Premium Upgrade")

        else:
            recommendations.append("🏆 Reward customer loyalty")
            recommendations.append("🎉 Give early access to new releases")
            if customer["Subscription_Plan"] != "Premium":
                recommendations.append("💎 Recommend Premium Upgrade")

    elif customer_stage == "existing":

        if probability >= 0.70:
            recommendations.append("🎁 Give long-term customer renewal discount")
            if customer["Customer_Satisfaction"] <= 4:
                recommendations.append("📞 Contact customer personally")
            if customer["Support_Queries"] >= 5:
                recommendations.append("🛠 Resolve customer complaints immediately")
            if customer["Days_Since_Last_Activity"] >= 30:
                recommendations.append("📧 Send 'We Miss You' email")
            recommendations.append("🏆 Offer exclusive loyalty benefits")
            if customer["Subscription_Plan"] == "Basic":
                recommendations.append("⭐ Offer Premium Trial")
            elif customer["Subscription_Plan"] == "Standard":
                recommendations.append("💎 Offer Premium Upgrade")

        elif probability >= 0.30:
            recommendations.append("🏆 Give long-term loyalty reward")
            recommendations.append("🎬 Recommend personalized content")
            if customer["Customer_Satisfaction"] <= 6:
                recommendations.append("😊 Improve customer experience")
            if customer["Subscription_Plan"] == "Basic":
                recommendations.append("⭐ Recommend Standard Plan")
            elif customer["Subscription_Plan"] == "Standard":
                recommendations.append("💎 Recommend Premium Upgrade")

        else:
            recommendations.append("🏆 Reward long-term customer loyalty")
            recommendations.append("🎉 Give early access to new releases")
            recommendations.append("💎 Offer exclusive customer benefits")
            if customer["Subscription_Plan"] != "Premium":
                recommendations.append("⭐ Recommend Premium Upgrade")

    return recommendations
